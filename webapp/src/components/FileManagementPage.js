import React, { useState, useEffect } from 'react';
import { useAuth } from '../AuthContext';
import axios from 'axios';

const FileManagementPage = () => {
  const { user, logout } = useAuth();
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  const [editingFile, setEditingFile] = useState(null);
  const [newFileName, setNewFileName] = useState('');

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

  const handleDownload = async (fileId, fileName) => {
    try {
      const response = await axios.get(`/api/files/${fileId}`, {
        responseType: 'blob', // Important for file downloads
      });
      
      // Create a temporary URL for the blob
      const blob = new Blob([response.data]);
      const url = window.URL.createObjectURL(blob);
      
      // Create a temporary link element and trigger download
      const link = document.createElement('a');
      link.href = url;
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      showMessage(`File "${fileName}" downloaded successfully`, 'success');
    } catch (error) {
      console.error('Download failed:', error);
      if (error.response?.status === 404) {
        showMessage('File not found or access denied', 'error');
      } else {
        showMessage('Failed to download file', 'error');
      }
    }
  };

  const handleUpload = () => {
    // Create a file input element
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*'; // Accept images only for now
    fileInput.onchange = async (event) => {
      const file = event.target.files[0];
      if (!file) return;

      try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await axios.post('/api/files/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        if (response.data.success) {
          showMessage(`File "${file.name}" uploaded successfully`, 'success');
          // Reload files to show the new one
          await loadFiles();
        }
      } catch (error) {
        console.error('Upload failed:', error);
        showMessage('Failed to upload file', 'error');
      }
    };
    fileInput.click();
  };

  const showMessage = (msg, type) => {
    setMessage(msg);
    setMessageType(type);
    setTimeout(() => {
      setMessage('');
      setMessageType('');
    }, 4000);
  };

  const handleRename = (fileId, currentName) => {
    console.log('handleRename called:', { fileId, currentName });
    setEditingFile(fileId);
    setNewFileName(currentName);
    console.log('State set:', { editingFile: fileId, newFileName: currentName });
  };

  const saveRename = async (fileId) => {
    if (!newFileName.trim()) {
      showMessage('Le nom du fichier ne peut pas être vide', 'error');
      return;
    }

    try {
      // Utilise POST au lieu de PATCH si PATCH pose problème
      const response = await axios.post(`/api/files/${fileId}/rename`, {
        new_name: newFileName.trim()
      });

      if (response.data.success) {
        showMessage(`Fichier renommé en "${response.data.new_display_name}"`, 'success');
        setEditingFile(null);
        setNewFileName('');
        loadFiles(); // Rafraîchir la liste
      }
    } catch (error) {
      console.error('Rename failed:', error);
      showMessage('Échec du renommage: ' + (error.response?.data?.detail || error.message), 'error');
    }
  };

  const cancelRename = () => {
    setEditingFile(null);
    setNewFileName('');
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
          📤 Upload Image
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
                {editingFile === file.id ? (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                    <input
                      key={`rename-input-${file.id}`}
                      type="text"
                      value={newFileName || ''}
                      onChange={(e) => {
                        console.log('Input change:', e.target.value);
                        setNewFileName(e.target.value);
                      }}
                      onInput={(e) => {
                        console.log('Input event:', e.target.value);
                        setNewFileName(e.target.value);
                      }}
                      style={{
                        padding: '8px !important',
                        border: '2px solid #007bff !important',
                        borderRadius: '4px !important',
                        fontSize: '14px !important',
                        flex: '1 !important',
                        width: 'auto !important',
                        outline: 'none !important',
                        backgroundColor: 'white !important',
                        color: 'black !important',
                        boxSizing: 'border-box !important',
                        minWidth: '200px !important'
                      }}
                      placeholder="Nouveau nom du fichier"
                      autoFocus={true}
                      disabled={false}
                      readOnly={false}
                      tabIndex={0}
                      onKeyDown={(e) => {
                        console.log('Key pressed:', e.key);
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          e.stopPropagation();
                          saveRename(file.id);
                        }
                        if (e.key === 'Escape') {
                          e.preventDefault();
                          e.stopPropagation();
                          cancelRename();
                        }
                      }}
                      onFocus={(e) => {
                        console.log('Input focused:', e.target.value);
                        setTimeout(() => e.target.select(), 0);
                      }}
                      onClick={(e) => {
                        console.log('Input clicked:', e.target.value);
                        e.stopPropagation();
                      }}
                      onMouseDown={(e) => {
                        e.stopPropagation();
                      }}
                    />
                    <button
                      onClick={() => saveRename(file.id)}
                      style={{
                        backgroundColor: '#28a745',
                        color: 'white',
                        border: 'none',
                        padding: '8px 12px',
                        borderRadius: '4px',
                        cursor: 'pointer'
                      }}
                    >
                      ✓
                    </button>
                    <button
                      onClick={cancelRename}
                      style={{
                        backgroundColor: '#6c757d',
                        color: 'white',
                        border: 'none',
                        padding: '8px 12px',
                        borderRadius: '4px',
                        cursor: 'pointer'
                      }}
                    >
                      ✗
                    </button>
                  </div>
                ) : (
                  <h4 
                    onClick={() => handleRename(file.id, file.name)}
                    style={{ 
                      cursor: 'pointer', 
                      color: '#007bff',
                      margin: '0 0 10px 0'
                    }}
                    title="Cliquer pour renommer"
                  >
                    📄 {file.name} ✏️
                  </h4>
                )}
                <p>Size: {file.size} • Uploaded: {file.uploaded}</p>
              </div>
              
              {editingFile !== file.id && (
                <div className="file-actions">
                  <button 
                    onClick={() => handleRename(file.id, file.name)}
                    style={{
                      backgroundColor: '#ffc107',
                      color: '#000',
                      border: 'none',
                      padding: '8px 15px',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      marginRight: '10px'
                    }}
                  >
                    ✏️ Renommer
                  </button>
                  <button 
                    onClick={() => handleDownload(file.id, file.name)}
                    className="btn-secondary"
                    style={{ marginRight: '10px' }}
                  >
                    📥 Download
                  </button>
                  <button 
                    onClick={() => handleDelete(file.id, file.name)}
                    className="btn-danger"
                  >
                    🗑️ Delete
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* System Info */}
      <div style={{ 
        marginTop: '30px', 
        padding: '15px', 
        background: '#e9ecef', 
        borderRadius: '6px',
        fontSize: '14px',
        color: '#666'
      }}>
        <strong>� System Status:</strong><br />
        • Real file storage using MongoDB GridFS<br />
        • User-specific file isolation and ownership<br />
        • JWT authentication protecting all file operations<br />
        • Total Files: {files.length}
      </div>
    </div>
  );
};

export default FileManagementPage;
