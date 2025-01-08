<template>
  <v-navigation-drawer color="#212121" title="Mycelium" permanent class="nav-drawer">
    <div class="logo-container">
      <img :src="logoSrc" alt="Logo" class="logo" height="60" />
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
  </v-navigation-drawer>
</template>

<script setup>
import { MENU_ITEMS } from '@/utils/constants'

const logoSrc = require('@/assets/logo.png')

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
}
</style>
