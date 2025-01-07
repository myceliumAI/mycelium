import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'
import { authService } from './services/auth.service'
import { validateConfig } from '@/utils/constants'

loadFonts()

const initApp = async () => {
  try {
    await authService.init()
    
    const app = createApp(App)
    app.use(vuetify)
    app.use(router)
    
    // Make auth service available globally
    app.config.globalProperties.$auth = authService
    
    // Validate configuration before app start
    if (!validateConfig()) {
      console.error('🚨 Application configuration is invalid')
      // Optionally handle the error (show error page, etc.)
    }
    
    app.mount('#app')
  } catch (error) {
    console.error('❌ Failed to initialize application:', error)
  }
}

initApp()

