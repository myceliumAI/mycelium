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
  
  const finalConfig = {
    KC_HOST: runtimeConfig?.KC_HOST || import.meta.env.VITE_KC_HOST,
    KC_PORT: runtimeConfig?.KC_PORT || import.meta.env.VITE_KC_PORT,
    KC_REALM: runtimeConfig?.KC_REALM || import.meta.env.VITE_KC_REALM,
    KC_CLIENT_ID: runtimeConfig?.KC_CLIENT_ID || import.meta.env.VITE_KC_CLIENT_ID
  };

  // console.log('Final config:', finalConfig);
  return finalConfig;
};

export const CONFIG = getRuntimeConfig();