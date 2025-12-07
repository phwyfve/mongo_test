#!/usr/bin/env python3
"""
Debug script to investigate tmp_files cleanup issues
This script will show what files exist and why they might not be cleaned up
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from cleanup_service import TmpFilesCleanupService
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

async def debug_tmp_files():
    """Debug what's in tmp_files and why cleanup isn't working"""
    
    print("🔍 Debugging tmp_files cleanup issues...")
    
    # Connect to database
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]
    
    cleanup_service = TmpFilesCleanupService()
    
    print("\n📊 === CURRENT TMP_FILES STATUS ===")
    
    # Get all files in tmp_files
    cursor = cleanup_service.tmp_bucket.find({})
    files_found = []
    
    async for file_doc in cursor:
        file_info = {
            "id": str(file_doc._id),
            "filename": file_doc.filename,
            "size_bytes": file_doc.length,
            "size_mb": round(file_doc.length / (1024 * 1024), 2),
            "upload_date": file_doc.upload_date,
            "age_hours": (datetime.utcnow() - file_doc.upload_date).total_seconds() / 3600,
            "metadata": getattr(file_doc, 'metadata', {})
        }
        files_found.append(file_info)
    
    print(f"Total files in tmp_files bucket: {len(files_found)}")
    
    if not files_found:
        print("✅ No files found in tmp_files - cleanup is working or no files uploaded!")
        return
    
    print(f"\n📋 === FILE DETAILS ===")
    for i, file_info in enumerate(files_found, 1):
        print(f"\n{i}. File ID: {file_info['id']}")
        print(f"   Filename: {file_info['filename']}")
        print(f"   Size: {file_info['size_mb']} MB")
        print(f"   Upload Date: {file_info['upload_date']}")
        print(f"   Age: {file_info['age_hours']:.1f} hours")
        if file_info['metadata']:
            print(f"   Metadata: {file_info['metadata']}")
    
    # Check cleanup thresholds
    print(f"\n⚙️ === CLEANUP SETTINGS ===")
    max_age_hours = getattr(settings, 'tmp_files_max_age_hours', 24)
    print(f"Time-based cleanup threshold: {max_age_hours} hours")
    print(f"Command-based cleanup threshold: 1 hour (for completed commands)")
    
    # Check which files would be cleaned by time-based cleanup
    cutoff_date = datetime.utcnow() - timedelta(hours=max_age_hours)
    time_cleanup_files = [f for f in files_found if f['upload_date'] < cutoff_date]
    
    print(f"\n🕒 === TIME-BASED CLEANUP ANALYSIS ===")
    print(f"Files older than {max_age_hours} hours (would be deleted): {len(time_cleanup_files)}")
    
    if time_cleanup_files:
        print("Files that SHOULD be deleted by time-based cleanup:")
        for f in time_cleanup_files:
            print(f"  - {f['filename']} (ID: {f['id']}, Age: {f['age_hours']:.1f}h)")
    else:
        oldest_file = min(files_found, key=lambda x: x['upload_date']) if files_found else None
        if oldest_file:
            print(f"Oldest file is only {oldest_file['age_hours']:.1f} hours old - not old enough to clean")
    
    # Check commands and their file associations
    print(f"\n🎯 === COMMAND-BASED CLEANUP ANALYSIS ===")
    
    # Find commands that reference files in tmp_files
    command_cursor = db.commands.find({})
    commands_with_files = []
    
    async for command in command_cursor:
        file_ids = command.get("args", {}).get("file_ids", [])
        if file_ids:
            command_info = {
                "command_id": str(command["_id"]),
                "shell_command": command.get("shell_command"),
                "exit_state": command.get("exit_state"),
                "completed_at": command.get("completed_at"),
                "file_ids": file_ids,
                "files_in_tmp": []
            }
            
            # Check which of these files actually exist in tmp_files
            for file_id in file_ids:
                if file_id in [f['id'] for f in files_found]:
                    matching_file = next(f for f in files_found if f['id'] == file_id)
                    command_info["files_in_tmp"].append(matching_file)
            
            if command_info["files_in_tmp"]:
                commands_with_files.append(command_info)
    
    print(f"Commands with files in tmp_files: {len(commands_with_files)}")
    
    for cmd in commands_with_files:
        print(f"\n  Command: {cmd['shell_command']} (ID: {cmd['command_id']})")
        print(f"    Exit State: {cmd['exit_state']} (-1=running, 0=success, >0=failed)")
        print(f"    Completed: {cmd['completed_at']}")
        print(f"    Files in tmp_files: {len(cmd['files_in_tmp'])}")
        
        for f in cmd['files_in_tmp']:
            print(f"      - {f['filename']} (Age: {f['age_hours']:.1f}h)")
        
        # Check if this command's files would be cleaned
        if cmd['exit_state'] != -1 and cmd['completed_at']:
            completion_age = (datetime.utcnow() - cmd['completed_at']).total_seconds() / 3600
            if completion_age > 1:
                print(f"    ✅ This command's files SHOULD be cleaned (completed {completion_age:.1f}h ago)")
            else:
                print(f"    ⏳ This command's files are too new to clean (completed {completion_age:.1f}h ago)")
        else:
            print(f"    ⏳ Command still running or no completion time")
    
    # Find orphaned files (not linked to any command)
    all_command_file_ids = []
    async for command in db.commands.find({}):
        file_ids = command.get("args", {}).get("file_ids", [])
        all_command_file_ids.extend(file_ids)
    
    orphaned_files = [f for f in files_found if f['id'] not in all_command_file_ids]
    
    print(f"\n🏷️ === ORPHANED FILES ANALYSIS ===")
    print(f"Files not linked to any command: {len(orphaned_files)}")
    
    if orphaned_files:
        print("Orphaned files (should be cleaned by time-based cleanup):")
        for f in orphaned_files:
            print(f"  - {f['filename']} (ID: {f['id']}, Age: {f['age_hours']:.1f}h)")
    
    # Suggestions
    print(f"\n💡 === CLEANUP SUGGESTIONS ===")
    
    if time_cleanup_files:
        print(f"🕒 Run time-based cleanup to remove {len(time_cleanup_files)} old files")
    
    if orphaned_files and not time_cleanup_files:
        print(f"🏷️ You have {len(orphaned_files)} orphaned files, but they're not old enough")
        print(f"   Consider reducing tmp_files_max_age_hours from {max_age_hours} to a lower value")
    
    completed_commands_with_old_files = [
        cmd for cmd in commands_with_files 
        if cmd['exit_state'] != -1 and cmd['completed_at'] 
        and (datetime.utcnow() - cmd['completed_at']).total_seconds() > 3600
    ]
    
    if completed_commands_with_old_files:
        print(f"🎯 Run command-based cleanup to remove files from {len(completed_commands_with_old_files)} completed commands")
    
    if not time_cleanup_files and not completed_commands_with_old_files and not orphaned_files:
        print("✅ All files are recent and properly linked - no cleanup needed")
    
    print(f"\n🧪 === MANUAL CLEANUP TEST ===")
    print("To test cleanup manually, run:")
    print("python test_cleanup.py")

if __name__ == "__main__":
    try:
        asyncio.run(debug_tmp_files())
    except KeyboardInterrupt:
        print("\n👋 Debug interrupted by user")
    except Exception as e:
        print(f"\n💥 Debug error: {e}")
        import traceback
        traceback.print_exc()
