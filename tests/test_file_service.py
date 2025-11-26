"""
Test script for GridFS file service functionality
"""
import asyncio
import pytest
from file_service import FileService
from database import init_db
from datetime import datetime
import io
import os

class TestFileService:
    """Test class for FileService"""
    
    def __init__(self):
        self.file_service = FileService()
        
    async def test_upload_and_download(self):
        """Test file upload and download functionality"""
        print("🧪 Testing file upload and download...")
        
        # Test data
        test_content = b"Hello, this is a test file content!"
        test_filename = "test_file.txt"
        test_metadata = {
            "owner": "test@example.com",
            "test_file": True,
            "created_at": datetime.utcnow().isoformat()
        }
        
        try:
            # Upload file
            file_id = await self.file_service.upload_file(
                filename=test_filename,
                content=test_content,
                content_type="text/plain",
                metadata=test_metadata
            )
            print(f"✅ File uploaded with ID: {file_id}")
            
            # Download file
            downloaded_content = await self.file_service.download_file(str(file_id))
            print(f"✅ File downloaded, size: {len(downloaded_content)} bytes")
            
            # Verify content
            assert downloaded_content == test_content, "Downloaded content doesn't match uploaded content"
            print("✅ Content verification passed")
            
            # Get file info
            file_info = await self.file_service.get_file_info(str(file_id))
            print(f"✅ File info retrieved: {file_info.get('filename')}")
            
            # Clean up - delete test file
            await self.file_service.delete_file(str(file_id))
            print("✅ Test file cleaned up")
            
            return True
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
    
    async def test_list_files(self):
        """Test listing files functionality"""
        print("🧪 Testing file listing...")
        
        try:
            # Upload a couple test files
            file_ids = []
            for i in range(3):
                file_id = await self.file_service.upload_file(
                    filename=f"test_list_{i}.txt",
                    content=f"Content of test file {i}".encode(),
                    content_type="text/plain",
                    metadata={"test_list": True, "index": i}
                )
                file_ids.append(str(file_id))
            
            print(f"✅ Uploaded {len(file_ids)} test files")
            
            # List files
            files = await self.file_service.list_files()
            print(f"✅ Retrieved file list, total files: {len(files)}")
            
            # Verify our test files are in the list
            test_files = [f for f in files if f.get("metadata", {}).get("test_list")]
            assert len(test_files) >= 3, f"Expected at least 3 test files, found {len(test_files)}"
            print("✅ Test files found in list")
            
            # Clean up test files
            for file_id in file_ids:
                await self.file_service.delete_file(file_id)
            print("✅ Test files cleaned up")
            
            return True
            
        except Exception as e:
            print(f"❌ List test failed: {e}")
            return False
    
    async def test_file_not_found(self):
        """Test handling of non-existent files"""
        print("🧪 Testing file not found scenarios...")
        
        try:
            fake_file_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format but non-existent
            
            # Try to get info for non-existent file
            file_info = await self.file_service.get_file_info(fake_file_id)
            assert file_info is None, "Expected None for non-existent file"
            print("✅ Non-existent file info handling correct")
            
            # Try to download non-existent file
            try:
                await self.file_service.download_file(fake_file_id)
                assert False, "Expected exception for non-existent file download"
            except Exception:
                print("✅ Non-existent file download properly raises exception")
            
            # Try to delete non-existent file
            try:
                await self.file_service.delete_file(fake_file_id)
                assert False, "Expected exception for non-existent file deletion"
            except Exception:
                print("✅ Non-existent file deletion properly raises exception")
            
            return True
            
        except Exception as e:
            print(f"❌ Not found test failed: {e}")
            return False

async def run_all_tests():
    """Run all file service tests"""
    print("🚀 Starting GridFS File Service Tests")
    print("=" * 50)
    
    try:
        # Initialize database
        await init_db()
        print("✅ Database initialized")
        
        # Create test instance
        test_service = TestFileService()
        
        # Run tests
        tests = [
            test_service.test_upload_and_download(),
            test_service.test_list_files(),
            test_service.test_file_not_found()
        ]
        
        results = await asyncio.gather(*tests, return_exceptions=True)
        
        # Check results
        passed = sum(1 for result in results if result is True)
        total = len(results)
        
        print("=" * 50)
        print(f"🏁 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("✅ All tests passed! GridFS FileService is working correctly.")
        else:
            print("❌ Some tests failed. Check the output above.")
            for i, result in enumerate(results):
                if result is not True:
                    print(f"   Test {i+1} result: {result}")
        
        return passed == total
        
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        return False

if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)
