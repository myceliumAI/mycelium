// Menu items and other static constants
export const MENU_ITEMS = [
  { icon: 'mdi-plus', title: 'New Chat', value: 'newChat' },
  { icon: 'mdi-pen', title: 'Create DataContract', value: 'createDataContract' },
  { icon: 'mdi-format-list-bulleted-square', title: 'List DataContracts', value: 'listDataContracts' }
];

// Runtime configuration with fallbacks to environment variables
const getRuntimeConfig = () => {
  // Check if we have runtime config from the injected script
  const runtimeConfig = window.__RUNTIME_CONFIG__;

  return {
    KC_URL: runtimeConfig?.KC_URL || process.env.KC_URL || 'http://localhost:8080',
    KC_REALM: runtimeConfig?.KC_REALM || process.env.KC_REALM || 'master',
    KC_CLIENT_ID: runtimeConfig?.KC_CLIENT_ID || process.env.KC_CLIENT_ID || 'mycelium'
  };
};

export const CONFIG = getRuntimeConfig();

// Add a helper to check if we're in development mode
export const isDevelopment = process.env.NODE_ENV === 'development';

// Optional: Add a configuration validation helper
export const validateConfig = () => {
  const requiredKeys = ['KC_URL', 'KC_REALM', 'KC_CLIENT_ID'];
  const missingKeys = requiredKeys.filter(key => !CONFIG[key]);
  
  if (missingKeys.length > 0) {
    console.error('❌ Missing required configuration:', missingKeys);
    return false;
  }
  
  console.log('✅ Configuration validated successfully');
  return true;
};
