import React, { useState } from 'react';
import { useAuth } from '../AuthContext';
import { Link } from 'react-router-dom';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    firstName: '',
    lastName: '',
    password: '',
    confirmPassword: ''
  });
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  const { register, loading } = useAuth();

  const validatePassword = (password) => {
    const errors = [];
    
    if (password.length < 6) {
      errors.push('Password must be at least 6 characters long');
    }
    
    if (!/[A-Z]/.test(password)) {
      errors.push('Password must contain at least one uppercase letter');
    }
    
    if (!/[a-z]/.test(password)) {
      errors.push('Password must contain at least one lowercase letter');
    }
    
    if (!/\d/.test(password)) {
      errors.push('Password must contain at least one number');
    }
    
    return errors;
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear specific error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }

    // Real-time password validation
    if (name === 'password') {
      const passwordErrors = validatePassword(value);
      setErrors(prev => ({
        ...prev,
        password: passwordErrors.length > 0 ? passwordErrors : ''
      }));
    }

    // Real-time confirm password validation
    if (name === 'confirmPassword') {
      if (value && value !== formData.password) {
        setErrors(prev => ({
          ...prev,
          confirmPassword: 'Passwords do not match'
        }));
      } else {
        setErrors(prev => ({
          ...prev,
          confirmPassword: ''
        }));
      }
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Name validation
    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required';
    }

    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required';
    }

    // Password validation
    const passwordErrors = validatePassword(formData.password);
    if (passwordErrors.length > 0) {
      newErrors.password = passwordErrors;
    }

    // Confirm password validation
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    return newErrors;
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    
    // Validate form
    const newErrors = validateForm();
    setErrors(newErrors);

    if (Object.keys(newErrors).length > 0) {
      setMessage('Please fix the errors below');
      setMessageType('error');
      return;
    }

    // Call register function
    const result = await register(formData.email, formData.password, formData.firstName, formData.lastName);
    
    if (result.success) {
      setMessage('Registration successful! Redirecting...', 'success');
    } else {
      setMessage(result.error || 'Registration failed', 'error');
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
        📝 Create Account
      </h2>
      
      <form onSubmit={handleRegister}>
        <div className="form-group">
          <label htmlFor="email">Email Address *</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            placeholder="Enter your email"
            disabled={loading}
            required
          />
          {errors.email && (
            <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
              {errors.email}
            </div>
          )}
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <div className="form-group" style={{ flex: 1 }}>
            <label htmlFor="firstName">First Name *</label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              value={formData.firstName}
              onChange={handleInputChange}
              placeholder="First name"
              disabled={loading}
              required
            />
            {errors.firstName && (
              <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
                {errors.firstName}
              </div>
            )}
          </div>

          <div className="form-group" style={{ flex: 1 }}>
            <label htmlFor="lastName">Last Name *</label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              value={formData.lastName}
              onChange={handleInputChange}
              placeholder="Last name"
              disabled={loading}
              required
            />
            {errors.lastName && (
              <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
                {errors.lastName}
              </div>
            )}
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="password">Password *</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleInputChange}
            placeholder="Enter your password"
            disabled={loading}
            required
          />
          {errors.password && (
            <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
              {Array.isArray(errors.password) ? (
                <ul style={{ margin: '0', paddingLeft: '20px' }}>
                  {errors.password.map((error, index) => (
                    <li key={index}>{error}</li>
                  ))}
                </ul>
              ) : (
                errors.password
              )}
            </div>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="confirmPassword">Confirm Password *</label>
          <input
            type="password"
            id="confirmPassword"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleInputChange}
            placeholder="Confirm your password"
            disabled={loading}
            required
          />
          {errors.confirmPassword && (
            <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
              {errors.confirmPassword}
            </div>
          )}
        </div>

        {message && (
          <div className={messageType === 'error' ? 'error' : 'success'}>
            {message}
          </div>
        )}

        <button 
          type="submit" 
          disabled={loading || Object.keys(validateForm()).length > 0}
        >
          {loading ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>

      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <p style={{ color: '#666' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: '#007bff', textDecoration: 'none' }}>
            Sign in here
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
        <strong>Password Requirements:</strong><br />
        • At least 6 characters long<br />
        • At least one uppercase letter (A-Z)<br />
        • At least one lowercase letter (a-z)<br />
        • At least one number (0-9)
      </div>
    </div>
  );
};

export default RegisterPage;
