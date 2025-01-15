<template>
  <v-btn
    icon="mdi-close"
    variant="text"
    class="ml-2"
    :title="title"
    @click="$emit('close')"
  />
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: 'Close'
  }
})

defineEmits(['close'])
</script> 