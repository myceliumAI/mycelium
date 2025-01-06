import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'
import { authService } from './services/auth.service'

loadFonts()

const initApp = async () => {
  try {
    await authService.init()
    
    const app = createApp(App)
    app.use(vuetify)
    app.use(router)
    
    // Make auth service available globally
    app.config.globalProperties.$auth = authService
    
    app.mount('#app')
  } catch (error) {
    console.error('❌ Failed to initialize application:', error)
  }
}

initApp()

