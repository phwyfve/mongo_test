import React, { useState, useEffect } from 'react';
import { useAuth } from '../AuthContext';
import axios from 'axios';

const FileManagementPage = () => {
  const { user, logout } = useAuth();
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/files');
      setFiles(response.data.files || []);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load files:', error);
      if (error.response?.status === 401) {
        showMessage('Session expired. Please login again.', 'error');
        logout();
      } else {
        showMessage('Failed to load files', 'error');
      }
      setLoading(false);
    }
  };

  const handleDelete = async (fileId, fileName) => {
    if (!window.confirm(`Are you sure you want to delete "${fileName}"?`)) {
      return;
    }

    try {
      const response = await axios.delete(`/api/files/${fileId}`);
      if (response.data.success) {
        showMessage(`File "${fileName}" deleted successfully`, 'success');
        // Remove from local state (since it's mocked)
        setFiles(files.filter(file => file.id !== fileId));
      }
    } catch (error) {
      console.error('Delete failed:', error);
      showMessage('Failed to delete file', 'error');
    }
  };

  const handleUpdate = async (fileId, fileName) => {
    try {
      const response = await axios.put(`/api/files/${fileId}`);
      if (response.data.success) {
        showMessage(`File "${fileName}" updated successfully`, 'success');
      }
    } catch (error) {
      console.error('Update failed:', error);
      showMessage('Failed to update file', 'error');
    }
  };

  const handleUpload = async () => {
    try {
      const response = await axios.post('/api/files/upload');
      if (response.data.success) {
        showMessage('File uploaded successfully', 'success');
        // Reload files to show the new one
        await loadFiles();
      }
    } catch (error) {
      console.error('Upload failed:', error);
      showMessage('Failed to upload file', 'error');
    }
  };

  const showMessage = (msg, type) => {
    setMessage(msg);
    setMessageType(type);
    setTimeout(() => {
      setMessage('');
      setMessageType('');
    }, 4000);
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading files...</div>
      </div>
    );
  }

  return (
    <div className="container">
      {/* User Info Header */}
      <div className="user-info">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2>📁 My Files</h2>
            <p>Welcome, {user?.first_name} {user?.last_name} ({user?.email})</p>
          </div>
          <button 
            onClick={logout}
            style={{ 
              width: 'auto', 
              padding: '8px 16px',
              background: '#dc3545'
            }}
          >
            Logout
          </button>
        </div>
      </div>

      {/* Messages */}
      {message && (
        <div className={messageType === 'error' ? 'error' : 'success'}>
          {message}
        </div>
      )}

      {/* Upload Button */}
      <div style={{ marginBottom: '20px' }}>
        <button 
          onClick={handleUpload}
          style={{ 
            width: 'auto', 
            padding: '10px 20px',
            background: '#28a745'
          }}
        >
          📤 Upload File (Mock)
        </button>
      </div>

      {/* Files List */}
      <div className="files-grid">
        {files.length === 0 ? (
          <div style={{ 
            textAlign: 'center', 
            padding: '40px',
            background: 'white',
            borderRadius: '10px',
            color: '#666'
          }}>
            <h3>No files found</h3>
            <p>Upload your first file to get started!</p>
          </div>
        ) : (
          files.map((file) => (
            <div key={file.id} className="file-item">
              <div className="file-info">
                <h4>📄 {file.name}</h4>
                <p>Size: {file.size} • Uploaded: {file.uploaded}</p>
              </div>
              <div className="file-actions">
                <button 
                  onClick={() => handleUpdate(file.id, file.name)}
                  className="btn-secondary"
                >
                  Edit
                </button>
                <button 
                  onClick={() => handleDelete(file.id, file.name)}
                  className="btn-danger"
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Debug Info */}
      <div style={{ 
        marginTop: '30px', 
        padding: '15px', 
        background: '#e9ecef', 
        borderRadius: '6px',
        fontSize: '14px',
        color: '#666'
      }}>
        <strong>🚧 Demo Mode:</strong><br />
        • Files are hardcoded mock data<br />
        • All file operations return success but don't actually do anything<br />
        • This demonstrates the protected routes working with JWT authentication<br />
        • Total Files: {files.length}
      </div>
    </div>
  );
};

export default FileManagementPage;
