"""
Test script for GridFS REST API endpoints
Tests the file management routes with authentication
"""
import requests
import json
import io
import os
from pathlib import Path

class TestFileAPI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.headers = {"Content-Type": "application/json"}
        
    def authenticate(self, email="testuser@example.com", password="testpass123"):
        """Authenticate and get JWT token"""
        print(f"🔐 Authenticating as {email}...")
        
        auth_data = {
            "email": email,
            "password": password,
            "first_name": "Test",
            "last_name": "User",
            "create": True
        }
        
        response = requests.post(f"{self.base_url}/api/authenticate", json=auth_data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                self.token = result.get("token")
                self.headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                }
                print(f"✅ Authentication successful")
                return True
        
        print(f"❌ Authentication failed: {response.text}")
        return False
    
    def test_list_files(self):
        """Test GET /api/files"""
        print("🧪 Testing file listing...")
        
        response = requests.get(f"{self.base_url}/api/files", headers=self.headers)
        
        if response.status_code == 200:
            result = response.json()
            files = result.get("files", [])
            print(f"✅ File list retrieved: {len(files)} files found")
            return True
        else:
            print(f"❌ File listing failed: {response.status_code} - {response.text}")
            return False
    
    def test_upload_file(self):
        """Test POST /api/files/upload"""
        print("🧪 Testing file upload...")
        
        # Create test file content
        test_content = "This is a test file for API testing!"
        test_filename = "api_test_file.txt"
        
        # Prepare file for upload
        files = {
            'file': (test_filename, io.StringIO(test_content), 'text/plain')
        }
        
        # Remove Content-Type for file upload (let requests handle it)
        upload_headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.post(
            f"{self.base_url}/api/files/upload",
            files=files,
            headers=upload_headers
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                file_id = result.get("file_id")
                print(f"✅ File uploaded successfully: ID = {file_id}")
                return file_id
        
        print(f"❌ File upload failed: {response.status_code} - {response.text}")
        return None
    
    def test_download_file(self, file_id):
        """Test GET /api/files/{file_id}"""
        print(f"🧪 Testing file download for ID: {file_id}...")
        
        response = requests.get(
            f"{self.base_url}/api/files/{file_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        if response.status_code == 200:
            content = response.content
            print(f"✅ File downloaded successfully: {len(content)} bytes")
            return True
        else:
            print(f"❌ File download failed: {response.status_code} - {response.text}")
            return False
    
    def test_get_file_info(self, file_id):
        """Test GET /api/files/{file_id}/info"""
        print(f"🧪 Testing file info for ID: {file_id}...")
        
        response = requests.get(
            f"{self.base_url}/api/files/{file_id}/info",
            headers=self.headers
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                file_info = result.get("file_info", {})
                filename = file_info.get("filename", "Unknown")
                print(f"✅ File info retrieved: {filename}")
                return True
        
        print(f"❌ File info failed: {response.status_code} - {response.text}")
        return False
    
    def test_delete_file(self, file_id):
        """Test DELETE /api/files/{file_id}"""
        print(f"🧪 Testing file deletion for ID: {file_id}...")
        
        response = requests.delete(
            f"{self.base_url}/api/files/{file_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print(f"✅ File deleted successfully")
                return True
        
        print(f"❌ File deletion failed: {response.status_code} - {response.text}")
        return False
    
    def test_file_not_found(self):
        """Test handling of non-existent files"""
        print("🧪 Testing file not found scenarios...")
        
        fake_file_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format
        
        # Test download non-existent file
        response = requests.get(
            f"{self.base_url}/api/files/{fake_file_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        if response.status_code == 404:
            print("✅ Non-existent file download returns 404")
            return True
        else:
            print(f"❌ Expected 404, got {response.status_code}")
            return False

def run_api_tests():
    """Run all API tests"""
    print("🚀 Starting GridFS REST API Tests")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/docs")
        if response.status_code != 200:
            print("❌ Server not running at http://localhost:8000")
            print("   Please start the server with: python main.py")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server at http://localhost:8000")
        print("   Please start the server with: python main.py")
        return False
    
    print("✅ Server is running")
    
    # Create test instance
    api_test = TestFileAPI()
    
    # Authenticate
    if not api_test.authenticate():
        print("❌ Authentication failed - cannot proceed with tests")
        return False
    
    # Run tests
    test_results = []
    
    # Test file listing
    test_results.append(api_test.test_list_files())
    
    # Test file upload
    file_id = api_test.test_upload_file()
    if file_id:
        test_results.append(True)
        
        # Test file info
        test_results.append(api_test.test_get_file_info(file_id))
        
        # Test file download
        test_results.append(api_test.test_download_file(file_id))
        
        # Test file deletion
        test_results.append(api_test.test_delete_file(file_id))
    else:
        test_results.extend([False, False, False, False])
    
    # Test not found scenarios
    test_results.append(api_test.test_file_not_found())
    
    # Calculate results
    passed = sum(test_results)
    total = len(test_results)
    
    print("=" * 50)
    print(f"🏁 API Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All API tests passed! GridFS REST endpoints working correctly.")
    else:
        print("❌ Some API tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    # Run the API tests
    success = run_api_tests()
    exit(0 if success else 1)
