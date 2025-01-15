<template>
  <v-navigation-drawer color="#212121" title="Mycelium" permanent class="nav-drawer">
    <div class="logo-container">
      <img src="/logo.png" alt="Logo" class="logo" height="60" />
    </div>
    <v-list nav>
      <v-list-item
        v-for="item in MENU_ITEMS"
        :key="item.value"
        :prepend-icon="item.icon"
        :title="item.title"
        :value="item.value"
        @click="handleItemClick(item.value)"
      ></v-list-item>
    </v-list>
    
    <!-- Add spacer to push logout to bottom -->
    <v-spacer></v-spacer>
    
    <!-- Logout button at bottom -->
    <v-list nav class="logout-section">
      <v-list-item
        prepend-icon="mdi-logout"
        title="Sign Out"
        @click="handleLogout"
      ></v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { MENU_ITEMS } from '@/utils/constants'
import keycloakService from '@/services/KeycloakService'

const emit = defineEmits(['newChat', 'createDataContract', 'listDataContracts'])

const handleItemClick = (value) => {
  switch (value) {
    case 'newChat':
      emit('newChat')
      break
    case 'createDataContract':
      emit('createDataContract')
      break
    case 'listDataContracts':
      emit('listDataContracts')
      break
  }
}

const handleLogout = async () => {
  try {
    await keycloakService.logout()
    console.log('✅ Successfully logged out')
  } catch (error) {
    console.error('❌ Logout failed:', error)
  }
}
</script>

<style scoped>
.logo-container {
  display: flex;
  justify-content: center;
  padding: 16px 0;
}

.nav-drawer {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.logout-section {
  margin-top: auto;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
}
</style>
