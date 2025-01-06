import { ref } from 'vue';
import Keycloak from 'keycloak-js';
import { CONFIG } from '@/utils/constants';

class AuthService {
  constructor() {
    this.keycloak = null;
    this.isAuthenticated = ref(false);
    this.userProfile = ref(null);
    this.error = ref(null);
  }

  async init() {
    try {
      this.keycloak = new Keycloak({
        url: CONFIG.KC_URL,
        realm: CONFIG.KC_REALM,
        clientId: CONFIG.KC_CLIENT_ID
      });

      const authenticated = await this.keycloak.init({
        onLoad: 'check-sso',
        silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html',
        pkceMethod: 'S256'
      });

      this.isAuthenticated.value = authenticated;
      
      if (authenticated) {
        await this.loadUserProfile();
        this.setupTokenRefresh();
      }

      console.log('✅ Keycloak initialized');
      return authenticated;
    } catch (error) {
      console.error('❌ Keycloak init error:', error);
      this.error.value = 'Failed to initialize authentication';
      throw error;
    }
  }

  async loadUserProfile() {
    try {
      this.userProfile.value = await this.keycloak.loadUserProfile();
      console.log('✅ User profile loaded');
    } catch (error) {
      console.error('❌ Error loading user profile:', error);
      throw error;
    }
  }

  setupTokenRefresh() {
    setInterval(() => {
      this.keycloak.updateToken(70).catch(() => {
        console.warn('⚠️ Failed to refresh token');
        this.logout();
      });
    }, 60000);
  }

  async login() {
    try {
      await this.keycloak.login();
    } catch (error) {
      console.error('❌ Login error:', error);
      throw error;
    }
  }

  async register() {
    try {
      await this.keycloak.register();
    } catch (error) {
      console.error('❌ Registration error:', error);
      throw error;
    }
  }

  async logout() {
    try {
      await this.keycloak.logout();
      this.isAuthenticated.value = false;
      this.userProfile.value = null;
    } catch (error) {
      console.error('❌ Logout error:', error);
      throw error;
    }
  }

  getToken() {
    return this.keycloak.token;
  }

  hasRole(role) {
    return this.keycloak.hasRealmRole(role);
  }
}

export const authService = new AuthService(); 