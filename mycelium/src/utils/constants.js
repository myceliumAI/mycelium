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
    BACKEND_HOST: runtimeConfig?.BACKEND_HOST || process.env.VUE_APP_BACKEND_HOST,
    KC_PORT: runtimeConfig?.KC_PORT || process.env.VUE_APP_KC_PORT,
    KC_REALM: runtimeConfig?.KC_REALM || process.env.VUE_APP_KC_REALM,
    KC_CLIENT_ID: runtimeConfig?.KC_CLIENT_ID || process.env.VUE_APP_KC_CLIENT_ID
  };
};

export const CONFIG = getRuntimeConfig();