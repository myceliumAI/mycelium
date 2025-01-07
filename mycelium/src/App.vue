<template>
  <v-app class="app-container">
    <v-app-bar v-if="keycloak.authenticated" app color="primary" dark>
      <v-toolbar-title>Mycelium</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="logout">Logout</v-btn>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import { defineComponent } from 'vue'
import { authService } from '@/services/auth.service'

export default defineComponent({
  name: 'App',
  setup() {
    const keycloak = authService.keycloak

    const logout = async () => {
      try {
        await keycloak.logout()
        console.log('✅ Successfully logged out')
      } catch (error) {
        console.error('❌ Failed to logout:', error)
      }
    }

    return {
      keycloak,
      logout
    }
  }
})
</script>

<style>
:root {
  --scrollbar-color: #212121;
}

html, body {
  height: 100%;
  overflow: hidden;
}

.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Global scrollbar styles */
* {
  scrollbar-width: thin;
  scrollbar-color: var(--scrollbar-color) transparent;
}

/* WebKit browsers (Chrome, Safari, etc.) */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: var(--scrollbar-color);
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: padding-box;
}

::-webkit-scrollbar-button {
  display: none;
}
</style>
