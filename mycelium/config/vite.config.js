import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true }),
    // Port webpack DefinePlugin settings
    {
      name: 'define-options',
      config() {
        return {
          define: {
            __VUE_PROD_DEVTOOLS__: false,
            __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
            __VUE_OPTIONS_API__: true,
            __VUE_PROD_TIPS__: false
          }
        }
      }
    }
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('../src', import.meta.url))
    }
  },
  server: {
    port: process.env.VITE_FRONTEND_PORT,
    proxy: {
      '/api': {
        target: `http://${process.env.VITE_API_HOST}:${process.env.VITE_API_PORT}`,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true
  }
})