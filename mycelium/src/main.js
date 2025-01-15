import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import keycloakService from '@/services/KeycloakService'
import vuetify from './plugins/vuetify'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

const initializeApp = async () => {
  try {
    const authenticated = await keycloakService.init()

    if (!authenticated) {
      window.location.reload()
      return
    }
    const app = createApp(App)

    app.config.globalProperties.$keycloak = keycloakService

    app.use(router)
    app.use(vuetify)
    app.mount('#app')

  } catch (error) {
    console.error(" ❌ Failed to initialize application:", error)
  }
}

initializeApp()
