import React, { useState } from 'react';
import { useAuth } from '../AuthContext';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'error' or 'success'
  const { login, register, loading } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    
    if (!email) {
      showMessage('Please enter your email', 'error');
      return;
    }

    const result = await login(email);
    
    if (result.success) {
      showMessage('Login successful! Redirecting...', 'success');
    } else {
      showMessage(result.error || 'Login failed', 'error');
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    
    if (!email) {
      showMessage('Please enter your email', 'error');
      return;
    }

    const result = await register(email);
    
    if (result.success) {
      showMessage('Registration successful! Redirecting...', 'success');
    } else {
      showMessage(result.error || 'Registration failed', 'error');
    }
  };

  const showMessage = (msg, type) => {
    setMessage(msg);
    setMessageType(type);
    setTimeout(() => {
      setMessage('');
      setMessageType('');
    }, 5000);
  };

  return (
    <div className="auth-container">
      <h2 style={{ textAlign: 'center', marginBottom: '30px', color: '#333' }}>
        📁 File Management System
      </h2>
      
      <form onSubmit={handleLogin}>
        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            disabled={loading}
            required
          />
        </div>

        {message && (
          <div className={messageType === 'error' ? 'error' : 'success'}>
            {message}
          </div>
        )}

        <button 
          type="submit" 
          disabled={loading}
          onClick={handleLogin}
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
        
        <button 
          type="button" 
          disabled={loading}
          onClick={handleRegister}
          style={{ background: '#28a745' }}
        >
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>

      <div style={{ 
        marginTop: '20px', 
        padding: '15px', 
        background: '#e9ecef', 
        borderRadius: '6px',
        fontSize: '14px',
        color: '#666'
      }}>
        <strong>Demo Mode:</strong><br />
        • Password is hardcoded as "password123"<br />
        • Just enter your email and click Login or Register<br />
        • Register works even if user already exists<br />
        • Try: outrunner@live.fr (existing user)
      </div>
    </div>
  );
};

export default LoginPage;
