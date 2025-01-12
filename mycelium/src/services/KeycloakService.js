import Keycloak from 'keycloak-js';
import { CONFIG } from '@/utils/constants';

/**
 * Service to handle Keycloak authentication and token management
 */
class KeycloakService {
    constructor() {
        /**
         * Initialize the Keycloak instance with configuration
         * @private
         */
        this.keycloak = new Keycloak({
            url: `http://${CONFIG.KC_HOST}:${CONFIG.KC_PORT}`,
            realm: CONFIG.KC_REALM,
            clientId: CONFIG.KC_CLIENT_ID,
        });

        // Bind methods to maintain context
        this.init = this.init.bind(this);
        this.updateToken = this.updateToken.bind(this);
        this.getToken = this.getToken.bind(this);
    }

    /**
     * Initialize Keycloak instance and authentication
     * @returns {Promise<void>}
     */
    async init() {
        try {
            const authenticated = await this.keycloak.init({
                onLoad: 'login-required',
                checkLoginIframe: false, // Disable iframe checking for better performance
                pkceMethod: 'S256' // Enable PKCE for better security
            });

            console.log('💡 Keycloak initialized:', authenticated ? '✅ Authenticated' : '❌ Not authenticated');

            // Set up token refresh
            this.setupTokenRefresh();

            // Set up logout event handler
            this.keycloak.onAuthLogout = () => {
                console.log('❌ User logged out');
                // Clear any stored tokens
                this.clearTokens();
            };

            return authenticated;
        } catch (error) {
            console.error('❌ Failed to initialize Keycloak:', error);
            throw error;
        }
    }

    /**
     * Set up automatic token refresh
     * @private
     */
    setupTokenRefresh() {
        // Refresh token 1 minute before it expires
        setInterval(() => {
            this.updateToken();
        }, 60000);
    }

    /**
     * Update the token if it's about to expire
     * @param {number} minValidity - Minimum validity time in seconds
     * @returns {Promise<boolean>}
     */
    async updateToken(minValidity = 70) {
        try {
            const refreshed = await this.keycloak.updateToken(minValidity);
            if (refreshed) {
                console.log('💡 Token refreshed');
            }
            return refreshed;
        } catch (error) {
            console.error('❌ Failed to refresh token:', error);
            // Redirect to login if token refresh fails
            await this.keycloak.login();
            return false;
        }
    }

    /**
     * Get the current access token
     * @returns {string|null}
     */
    getToken() {
        return this.keycloak.token;
    }

    /**
     * Get authorization headers for API requests
     * @returns {Object}
     */
    getAuthHeader() {
        return {
            Authorization: `Bearer ${this.getToken()}`
        };
    }

    /**
     * Check if the user is authenticated
     * @returns {boolean}
     */
    isAuthenticated() {
        return !!this.keycloak.authenticated;
    }

    /**
     * Get the authenticated user's profile
     * @returns {Promise<Object>}
     */
    async getUserProfile() {
        try {
            return await this.keycloak.loadUserProfile();
        } catch (error) {
            console.error('❌ Failed to load user profile:', error);
            throw error;
        }
    }

    /**
     * Logout the current user
     * @returns {Promise<void>}
     */
    async logout() {
        try {
            await this.keycloak.logout();
            this.keycloak.clearToken();
            console.log('✅ Successfully logged out')
        } catch (error) {
            console.error('❌ Failed to logout:', error);
            throw error;
        }
    }
}

// Create and export a singleton instance
const keycloakService = new KeycloakService();
export default keycloakService; 