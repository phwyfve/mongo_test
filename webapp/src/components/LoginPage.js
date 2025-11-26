import React, { useState } from 'react';
import { useAuth } from '../AuthContext';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'error' or 'success'
  const { login, register, loading } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    
    if (!email) {
      showMessage('Please enter your email', 'error');
      return;
    }

    if (!password) {
      showMessage('Please enter your password', 'error');
      return;
    }

    const result = await login(email, password);
    
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

    if (!password) {
      showMessage('Please enter your password', 'error');
      return;
    }

    if (password.length < 6) {
      showMessage('Password must be at least 6 characters long', 'error');
      return;
    }

    const result = await register(email, password);
    
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

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            disabled={loading}
            required
            minLength="6"
          />
        </div>

        {message && (
          <div className={messageType === 'error' ? 'error' : 'success'}>
            {message}
          </div>
        )}

        <button 
          type="submit" 
          disabled={loading || !email.trim() || !password.trim()}
          onClick={handleLogin}
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
        
        <button 
          type="button" 
          disabled={loading || !email.trim() || !password.trim() || password.length < 6}
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
        <strong>Security Notes:</strong><br />
        • Password must be at least 6 characters<br />
        • Existing users with default password "password123" can continue to use it<br />
        • New users must create their own password<br />
        • Try existing user: test2@hotmail.com (password: password123)
      </div>
    </div>
  );
};

export default LoginPage;
