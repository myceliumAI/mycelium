<template>
  <div class="side-panel-content">
    <div class="panel-header">
      <h2>{{ title }}</h2>
      <div class="header-actions">
        <slot name="header-actions">
          <CloseButton @close="$emit('close')" />
        </slot>
      </div>
    </div>

    <div class="panel-content">
      <slot></slot>
    </div>

    <div v-if="$slots['footer']" class="panel-footer">
      <div class="footer-content">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import CloseButton from './components/CloseButton.vue'

defineProps({
  title: {
    type: String,
    required: true
  }
})

defineEmits(['close'])
</script>

<style scoped>
.side-panel-content {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.header-actions {
  display: flex;
  align-items: center;
}

.panel-content {
  flex: 1;
  overflow: auto;
  padding: 16px;
}

.panel-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.12);
  padding: 16px;
  background: var(--v-surface-variant);
}

.footer-content {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}
</style> 