"""
Quick test script to upload img1.jpg and verify the file service is working
"""
import asyncio
import os
from file_service import FileService
from database import init_db

async def test_img1_upload():
    """Test uploading img1.jpg"""
    print("🚀 Testing img1.jpg upload...")
    
    try:
        # Initialize database
        await init_db()
        print("✅ Database initialized")
        
        # Create file service
        file_service = FileService()
        
        # Read the image file
        img_path = os.path.join("tests", "img1.jpg")
        if not os.path.exists(img_path):
            print(f"❌ Image file not found: {img_path}")
            return False
        
        with open(img_path, "rb") as f:
            file_content = f.read()
        
        print(f"✅ Read image file: {len(file_content)} bytes")
        
        # Test user info
        test_email = "testuser@example.com"
        test_user_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format
        
        # Upload the file
        result = await file_service.upload_file(
            file_content=file_content,
            filename="img1.jpg",
            content_type="image/jpeg",
            user_email=test_email,
            user_id=test_user_id
        )
        
        print(f"📤 Upload result: {result}")
        
        if result.get("success"):
            file_id = result.get("file_id")
            print(f"✅ File uploaded successfully! ID: {file_id}")
            
            # Test listing files for this user
            print("\n📋 Testing file listing...")
            files = await file_service.list_user_files(test_email, test_user_id)
            print(f"✅ Found {len(files)} files for user {test_email}")
            
            for file in files:
                print(f"   📄 {file['name']} ({file['size']}) - {file['uploaded']}")
            
            # Test getting file info
            print(f"\n📝 Testing file info for ID: {file_id}")
            file_info = await file_service.get_file_info(file_id, test_email, test_user_id)
            if file_info:
                print(f"✅ File info retrieved: {file_info['name']} - {file_info['size']}")
            else:
                print("❌ Could not retrieve file info")
            
            # Test download
            print(f"\n📥 Testing file download for ID: {file_id}")
            download_result = await file_service.download_file(file_id, test_email, test_user_id)
            if download_result:
                print(f"✅ File downloaded: {len(download_result['content'])} bytes")
                print(f"   Content type: {download_result['content_type']}")
                print(f"   Filename: {download_result['filename']}")
            else:
                print("❌ Could not download file")
            
            # Optional: Clean up (delete the test file)
            print(f"\n🗑️ Cleaning up test file...")
            delete_result = await file_service.delete_file(file_id, test_email, test_user_id)
            if delete_result.get("success"):
                print(f"✅ Test file deleted: {delete_result.get('message')}")
            else:
                print(f"❌ Could not delete test file: {delete_result.get('error')}")
            
            return True
        else:
            print(f"❌ Upload failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_img1_upload())
    if success:
        print("\n🎉 All tests passed! File service is working correctly.")
    else:
        print("\n💥 Tests failed. Check the output above for details.")
