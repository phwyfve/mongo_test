"""
MergePdfs API route
Handles PDF file upload and merge command creation
"""

import asyncio
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import List
from models import User
from auth import current_active_user
from file_service import FileService
from process_manager import create_command, process_command

router = APIRouter()

@router.post("/mergePdfs")
async def merge_pdfs_endpoint(
    files: List[UploadFile] = File(...),
    user: User = Depends(current_active_user)
):
    """
    Upload PDF files and create a merge command
    
    Steps:
    1. Validate uploaded files are PDFs
    2. Store files in GridFS tmp_files bucket
    3. Create merge command with file IDs
    4. Start command processing asynchronously
    5. Return command ID for polling
    """
    
    if len(files) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least 2 PDF files are required for merging"
        )
    
    # Validate all files are PDFs
    for file in files:
        if not file.content_type or not file.content_type.startswith('application/pdf'):
            raise HTTPException(
                status_code=400,
                detail=f"File '{file.filename}' is not a PDF. Only PDF files are allowed."
            )
    
    try:
        file_service = FileService()
        uploaded_file_ids = []
        
        # Upload each file to GridFS tmp_files bucket
        for file in files:
            # Read file content
            content = await file.read()
            
            if len(content) == 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"File '{file.filename}' is empty"
                )
            
            # Upload to tmp_files bucket (different from user files)
            # We'll use a separate GridFS bucket for temporary processing files
            result = await file_service.upload_temp_file(
                file_content=content,
                filename=file.filename,
                content_type=file.content_type,
                user_email=user.email,
                user_id=str(user.id)
            )
            
            if not result.get("success"):
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to upload file '{file.filename}': {result.get('error')}"
                )
            
            uploaded_file_ids.append(result["file_id"])
        
        # Create merge command
        command_id = await create_command(
            shell_command="MergePdfs",
            args={
                "file_ids": uploaded_file_ids,
                "user_id": str(user.id),
                "user_email": user.email
            }
        )
        
        # Start command processing asynchronously
        # This will run in the background and not block the response
        asyncio.create_task(process_command(command_id))
        
        return {
            "success": True,
            "command_id": command_id,
            "message": f"PDF merge started for {len(files)} files",
            "uploaded_files": [
                {"filename": f.filename, "file_id": fid} 
                for f, fid in zip(files, uploaded_file_ids)
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF merge request: {str(e)}"
        )
