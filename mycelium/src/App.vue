<template>
  <v-app class="app-container">
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App',
  setup() {
    return {}
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
