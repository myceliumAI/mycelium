<template>
  <v-btn
    icon="mdi-close"
    variant="text"
    @click="$emit('close')"
    class="ml-2"
    :title="title"
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