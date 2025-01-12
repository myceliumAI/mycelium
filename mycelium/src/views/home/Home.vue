<template>
  <div class="home-layout">
    <!-- Navigation Bar (10%) -->
    <NavBar
      @new-chat="handleNewChat"
      @create-data-contract="handleCreateDataContract"
      @list-data-contracts="handleListDataContracts"
      class="nav-bar"
    />

    <!-- Main Content Area (90%) -->
    <div class="main-content">
      <!-- Chat Area (50% or 100% depending on side panel) -->
      <ChatColumn
        ref="chatColumn"
        class="chat-column"
        :class="{ 'full-width': !isSidePanelOpen }"
      />

      <!-- Side Panel (50% when open) -->
      <transition name="slide">
        <div v-if="isSidePanelOpen" class="side-panel-container">
          <component
            :is="currentSidePanelComponent"
            @close="closeSidePanel"
            @contract-added="handleContractAdded"
          />
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NavBar from '@/components/navigation/NavBar.vue'
import ChatColumn from '@/components/chat/ChatColumn.vue'
import DataContract from '@/components/dataContract/DataContract.vue'
import ListDataContracts from '@/components/listDataContracts/ListDataContracts.vue'

defineOptions({
  name: 'HomePage',
  components: {
    DataContract,
    ListDataContracts
  }
})

const isSidePanelOpen = ref(false)
const currentSidePanelComponent = ref(null)
const chatColumn = ref(null)

const openSidePanel = (component) => {
  currentSidePanelComponent.value = component
  isSidePanelOpen.value = true
}

const closeSidePanel = () => {
  isSidePanelOpen.value = false
  currentSidePanelComponent.value = null
}

const handleNewChat = () => {
  closeSidePanel()
  chatColumn.value?.clearChat()
}

const handleCreateDataContract = () => {
  openSidePanel('DataContract')
}

const handleListDataContracts = () => {
  openSidePanel('ListDataContracts')
}

const handleContractAdded = () => {
  // Handle contract added event if needed
}
</script>

<style scoped>
.home-layout {
  height: 100vh;
  display: flex;
  overflow: hidden;
}

.nav-bar {
  flex: 0 0 10%;
  min-width: 200px;
  max-width: 300px;
  border-right: 1px solid rgba(0, 0, 0, 0.12);
}

.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.chat-column {
  flex: 0 0 50%;
  transition: flex 0.3s ease;
  overflow: hidden;
}

.chat-column.full-width {
  flex: 0 0 100%;
}

.side-panel-container {
  flex: 0 0 50%;
  overflow: hidden;
  border-left: 1px solid rgba(0, 0, 0, 0.12);
  background-color: var(--v-surface-variant);
}

/* Transition animations */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}

.slide-enter-to,
.slide-leave-from {
  transform: translateX(0);
}
</style>
