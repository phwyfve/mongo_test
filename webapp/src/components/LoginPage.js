import React, { useState } from 'react';
import { useAuth } from '../AuthContext';
import { Link } from 'react-router-dom';

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
        � Sign In
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
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>

      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <p style={{ color: '#666' }}>
          Don't have an account yet?{' '}
          <Link to="/register" style={{ color: '#007bff', textDecoration: 'none' }}>
            Create one here
          </Link>
        </p>
      </div>

      <div style={{ 
        marginTop: '20px', 
        padding: '15px', 
        background: '#e9ecef', 
        borderRadius: '6px',
        fontSize: '14px',
        color: '#666'
      }}>
        <strong>Demo Account:</strong><br />
        • Email: test2@hotmail.com<br />
        • Password: password123<br />
        • This is an existing user you can use for testing
      </div>
    </div>
  );
};

export default LoginPage;
