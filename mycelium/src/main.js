import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import App from './App.vue'
import router from './router'
import keycloakService from '@/services/KeycloakService'

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify Configuration
const vuetify = createVuetify({
  // Your vuetify options here
})

// Initialize the application
const initializeApp = async () => {
  try {
    // Initialize Keycloak
    const authenticated = await keycloakService.init()

    if (!authenticated) {
      window.location.reload()
      return
    }

    // Create Vue application
    const app = createApp(App)

    // Add KeycloakService instance to the global properties
    app.config.globalProperties.$keycloak = keycloakService

    // Use plugins
    app.use(router)
    app.use(vuetify)

    // Mount the app
    app.mount('#app')

  } catch (error) {
    console.error(" ❌ Failed to initialize application:", error)
  }
}

// Start the application
initializeApp()
