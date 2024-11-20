import axios from 'axios';

class AuthService {
  constructor() {
    this.isAuthenticated = false;
    this.user = null;
    
    // Add axios interceptor for handling 401 responses
    axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          this.isAuthenticated = false;
          this.user = null;
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  async login(username, password, mfaCode = null) {
    try {
      const response = await axios.post('/api/auth/login', {
        username,
        password,
        mfa_code: mfaCode
      });
      
      this.isAuthenticated = true;
      this.user = response.data.user;
      
      return response.data;
    } catch (error) {
      console.error(' ❌ Login failed:', error);
      throw error;
    }
  }

  async register(userData) {
    try {
      const response = await axios.post('/api/auth/register', userData);
      return response.data;
    } catch (error) {
      console.error(' ❌ Registration failed:', error);
      throw error;
    }
  }

  async logout() {
    try {
      await axios.post('/api/auth/logout');
      this.isAuthenticated = false;
      this.user = null;
    } catch (error) {
      console.error(' ❌ Logout failed:', error);
      throw error;
    }
  }

  async getCurrentUser() {
    try {
      const response = await axios.get('/api/auth/me');
      this.user = response.data.user;
      this.isAuthenticated = true;
      return this.user;
    } catch (error) {
      this.isAuthenticated = false;
      this.user = null;
      throw error;
    }
  }

  async checkMfaRequired(username) {
    try {
      const response = await axios.post('/api/auth/check-mfa', { username });
      return response.data.mfa_required;
    } catch (error) {
      console.error(' ❌ MFA check failed:', error);
      throw error;
    }
  }
}

export default new AuthService();
