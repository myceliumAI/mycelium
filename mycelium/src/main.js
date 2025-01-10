import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'
import keycloakService from './services/KeycloakService'

loadFonts()

const initApp = async () => {
  try {
    // Initialize Keycloak
    await keycloakService.init()
    
    // Create and mount Vue app only after Keycloak is initialized
    const app = createApp(App)
    
    // Make keycloakService available globally
    app.config.globalProperties.$keycloak = keycloakService
    
    app.use(vuetify)
    app.use(router)
    
    // Add navigation guard to check authentication
    router.beforeEach((to, from, next) => {
      if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!keycloakService.isAuthenticated()) {
          // Redirect to Keycloak login
          keycloakService.keycloak.login()
        } else {
          next()
        }
      } else {
        next()
      }
    })
    
    app.mount('#app')
    
    console.log('✅ Application initialized successfully')
  } catch (error) {
    console.error('❌ Failed to initialize application:', error)
  }
}

initApp()
