import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check for existing token on app start
  useEffect(() => {
    const savedToken = sessionStorage.getItem('auth_token');
    const savedUser = sessionStorage.getItem('user_data');
    
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
      
      // Set axios default header
      axios.defaults.headers.common['Authorization'] = `Bearer ${savedToken}`;
      
      // Validate token with server
      validateToken(savedToken)
        .then((isValid) => {
          if (!isValid) {
            logout();
          }
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const validateToken = async (token) => {
    try {
      // Use the correct endpoint for token validation
      const response = await axios.get('/api/user-profile', {
        headers: { Authorization: `Bearer ${token}` }
      });
      return response.status === 200;
    } catch (error) {
      console.log('Token validation failed:', error.response?.status, error.response?.data);
      return false;
    }
  };

  const login = async (email) => {
    setLoading(true);
    try {
      // First try to login with existing user
      const response = await axios.post('/api/authenticate', {
        email: email,
        password: 'password123', // Hardcoded password
        first_name: 'User',
        last_name: 'Name',
        create: false // Don't create, just try to login
      });

      if (response.data.success) {
        const { token, user_profile } = response.data;
        
        // Save to session storage
        sessionStorage.setItem('auth_token', token);
        sessionStorage.setItem('user_data', JSON.stringify(user_profile));
        
        // Update state
        setToken(token);
        setUser(user_profile);
        
        // Set axios default header
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        return { success: true };
      } else {
        return { success: false, error: response.data.error };
      }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      };
    } finally {
      setLoading(false);
    }
  };

  const register = async (email) => {
    setLoading(true);
    try {
      const response = await axios.post('/api/register', {
        email: email,
        password: 'password123', // Hardcoded password
        first_name: 'New',
        last_name: 'User'
      });

      if (response.data.success) {
        const { token, user_profile } = response.data;
        
        // Save to session storage
        sessionStorage.setItem('auth_token', token);
        sessionStorage.setItem('user_data', JSON.stringify(user_profile));
        
        // Update state
        setToken(token);
        setUser(user_profile);
        
        // Set axios default header
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        return { success: true };
      } else {
        return { success: false, error: response.data.error };
      }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    // Clear storage
    sessionStorage.removeItem('auth_token');
    sessionStorage.removeItem('user_data');
    
    // Clear state
    setToken(null);
    setUser(null);
    
    // Clear axios header
    delete axios.defaults.headers.common['Authorization'];
  };

  const value = {
    user,
    token,
    loading,
    isAuthenticated: !!token,
    login,
    register,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
