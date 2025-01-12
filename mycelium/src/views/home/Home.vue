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
    <div class="main-content" ref="mainContent">
      <!-- Chat Area -->
      <div 
        class="chat-container" 
        :class="{ 'resizing': isResizing }"
        :style="chatContainerStyle"
      >
        <ChatColumn
          ref="chatColumn"
          class="chat-column"
          :class="{ 'full-width': !isSidePanelOpen }"
        />

        <!-- Resizer -->
        <div
          v-if="isSidePanelOpen"
          class="resizer"
          @mousedown.prevent="startResize"
          title="Drag to resize"
        >
          <div class="resizer-handle"></div>
        </div>
      </div>

      <!-- Side Panel -->
      <transition name="slide">
        <div 
          v-if="isSidePanelOpen" 
          class="side-panel-container"
          :class="{ 'resizing': isResizing }"
          :style="sidePanelStyle"
        >
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
import { ref, computed } from 'vue'
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

// Panel width constants
const PANEL_DEFAULTS = Object.freeze({
  DEFAULT_WIDTH: 60,
  MIN_WIDTH: 30,
  MAX_WIDTH: 70
})

const isSidePanelOpen = ref(false)
const currentSidePanelComponent = ref(null)
const chatColumn = ref(null)
const mainContent = ref(null)
const chatWidth = ref(PANEL_DEFAULTS.DEFAULT_WIDTH)
const isResizing = ref(false)

// Computed styles for dynamic widths
const chatContainerStyle = computed(() => ({
  width: isSidePanelOpen.value ? `${chatWidth.value}%` : '100%'
}))

const sidePanelStyle = computed(() => ({
  width: `${100 - chatWidth.value}%`
}))

// Resizing functionality
const startResize = (e) => {
  e.preventDefault()
  isResizing.value = true
  
  const handleMouseMove = (e) => {
    if (!mainContent.value) return
    
    const bounds = mainContent.value.getBoundingClientRect()
    const x = e.clientX - bounds.left
    const totalWidth = bounds.width
    
    // Calculate percentage using constants
    let newWidth = (x / totalWidth) * 100
    newWidth = Math.max(
      PANEL_DEFAULTS.MIN_WIDTH, 
      Math.min(PANEL_DEFAULTS.MAX_WIDTH, newWidth)
    )
    
    requestAnimationFrame(() => {
      chatWidth.value = newWidth
    })
  }

  const handleMouseUp = () => {
    isResizing.value = false
    document.removeEventListener('mousemove', handleMouseMove)
    document.removeEventListener('mouseup', handleMouseUp)
    document.body.style.userSelect = ''
  }

  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
  document.body.style.userSelect = 'none'
}

const openSidePanel = (component) => {
  currentSidePanelComponent.value = component
  isSidePanelOpen.value = true
  chatWidth.value = PANEL_DEFAULTS.DEFAULT_WIDTH // Using constant
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
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 256px;
  z-index: 1004;
}

.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.chat-container {
  height: 100%;
  position: relative;
  display: flex;
  transition: width 0.15s ease-out;
}

.chat-column {
  width: 100%;
  height: 100%;
}

.side-panel-container {
  height: 100%;
  transition: width 0.15s ease-out;
}

.resizer {
  position: absolute;
  top: 0;
  bottom: 0;
  right: 0;
  width: 10px;
  cursor: col-resize;
  display: flex;
  justify-content: center;
  align-items: stretch;
  z-index: 10;
}

.resizer-handle {
  width: 4px;
  background-color: rgba(0, 0, 0, 0.12);
  transition: background-color 0.3s ease;
}

.resizer:hover .resizer-handle,
.resizer:active .resizer-handle {
  background-color: var(--v-primary-base);
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

/* Remove transition during active resizing */
.chat-container.resizing,
.side-panel-container.resizing {
  transition: none;
}
</style>