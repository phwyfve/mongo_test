#!/usr/bin/env python3
"""
Manual cleanup script for testing
Run this script to test the cleanup functionality without the web server
"""

import asyncio
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from cleanup_service import TmpFilesCleanupService

async def main():
    """Test cleanup functionality"""
    
    cleanup_service = TmpFilesCleanupService()
    
    print("🔍 Getting cleanup statistics...")
    stats = await cleanup_service.get_cleanup_stats()
    
    if stats["success"]:
        print(f"📊 Current tmp_files status:")
        print(f"   Total files: {stats['total_files']}")
        print(f"   Total size: {stats['total_size_mb']} MB")
        print(f"   Files by age:")
        for age_group, count in stats['files_by_age'].items():
            print(f"     {age_group}: {count} files")
    else:
        print(f"❌ Failed to get stats: {stats.get('error', 'Unknown error')}")
        return
    
    if stats['total_files'] == 0:
        print("✅ No temporary files to clean up!")
        return
    
    # Ask user what cleanup to run
    print("\n🧹 Cleanup options:")
    print("1. Time-based cleanup (delete files older than 24 hours)")
    print("2. Command-based cleanup (delete files for completed commands)")
    print("3. Full cleanup (both methods)")
    print("4. Emergency cleanup (delete ALL files)")
    print("5. Exit without cleaning")
    
    try:
        choice = input("\nEnter your choice (1-5): ").strip()
    except KeyboardInterrupt:
        print("\n👋 Cleanup cancelled by user")
        return
    
    if choice == "1":
        print("\n⏰ Running time-based cleanup...")
        result = await cleanup_service.cleanup_old_files(max_age_hours=24)
        
    elif choice == "2":
        print("\n🎯 Running command-based cleanup...")
        result = await cleanup_service.cleanup_by_command_status()
        
    elif choice == "3":
        print("\n🚀 Running full cleanup...")
        result = await cleanup_service.full_cleanup(max_age_hours=24)
        
    elif choice == "4":
        confirm = input("⚠️  EMERGENCY CLEANUP will delete ALL files. Type 'YES' to confirm: ")
        if confirm == "YES":
            print("\n🚨 Running emergency cleanup...")
            result = await cleanup_service.cleanup_old_files(max_age_hours=0)
        else:
            print("❌ Emergency cleanup cancelled")
            return
            
    elif choice == "5":
        print("👋 Exiting without cleanup")
        return
        
    else:
        print("❌ Invalid choice")
        return
    
    # Display results
    if result["success"]:
        if "total_deleted_files" in result:  # Full cleanup
            print(f"\n✅ Cleanup completed!")
            print(f"   Total files deleted: {result['total_deleted_files']}")
            print(f"   Total space freed: {result['total_size_freed_mb']} MB")
        else:  # Single cleanup method
            print(f"\n✅ Cleanup completed!")
            print(f"   Files deleted: {result['deleted_count']}")
            print(f"   Space freed: {result['total_size_freed_mb']} MB")
    else:
        print(f"\n❌ Cleanup failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Script interrupted by user")
    except Exception as e:
        print(f"\n💥 Script error: {e}")
