import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'

loadFonts()

const initApp = async () => {
  try {
    const app = createApp(App)
    app.use(vuetify)
    app.use(router)
    app.mount('#app')
  } catch (error) {
    console.error('❌ Failed to initialize application:', error)
  }
}

initApp()
