#!/usr/bin/env python3
"""
Python shell dispatcher for JSON-driven commands
Usage: python myshell.py <command_id>
"""

import sys
import asyncio
import json
import traceback
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from gridfs import GridFS
from bson import ObjectId
from tools_commands.tools_commands import commands
from config import settings

async def main():
    """Main entry point for command execution"""
    if len(sys.argv) < 2:
        print("Error: command_id is required", file=sys.stderr)
        sys.exit(1)
    
    command_id = sys.argv[1]
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(settings.database_url)
        db = client[settings.database_name]
        
        # Load command from database
        command_doc = await db.commands.find_one({"_id": ObjectId(command_id)})
        if not command_doc:
            print(f"Error: Command {command_id} not found", file=sys.stderr)
            sys.exit(1)
        
        shell_command = command_doc.get("shell_command")
        args = command_doc.get("args", {})
        
        # Look up handler
        if shell_command not in commands:
            print(f"Error: Unknown command '{shell_command}'", file=sys.stderr)
            sys.exit(1)
        
        handler = commands[shell_command]
        
        # Setup GridFS - use pymongo for GridFS since it needs sync client
        sync_client = pymongo.MongoClient(settings.database_url)
        sync_db = sync_client[settings.database_name]
        fs = GridFS(sync_db, collection="tmp_files")
        
        # Execute handler
        print(f"Executing command: {shell_command}")
        print(f"Args: {json.dumps(args, indent=2)}")
        
        result = await handler(args, db, fs)
        
        # Update command with success
        await db.commands.update_one(
            {"_id": ObjectId(command_id)},
            {
                "$set": {
                    "exit_state": 0,
                    "stdout": json.dumps(result, indent=2),
                    "stderr": None
                }
            }
        )
        
        print("Command completed successfully")
        print(f"Result: {json.dumps(result, indent=2)}")
        
    except Exception as e:
        # Update command with error
        error_msg = f"Command failed: {str(e)}"
        stderr_output = f"{error_msg}\n\nTraceback:\n{traceback.format_exc()}"
        
        try:
            client = AsyncIOMotorClient(settings.database_url)
            db = client[settings.database_name]
            await db.commands.update_one(
                {"_id": ObjectId(command_id)},
                {
                    "$set": {
                        "exit_state": 1,
                        "stdout": None,
                        "stderr": stderr_output
                    }
                }
            )
        except Exception as update_error:
            print(f"Failed to update command status: {update_error}", file=sys.stderr)
        
        print(error_msg, file=sys.stderr)
        print(f"Full traceback:\n{traceback.format_exc()}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
