<template>
  <div class="message-container" :class="{ 'user-message': isUser }">
    <div class="message-bubble" :class="{ 'user-bubble': isUser, 'ai-bubble': !isUser }">
      <div class="message-content" v-html="renderedMarkdown"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  message: {
    type: String,
    required: true
  },
  isUser: {
    type: Boolean,
    default: false
  }
})

const renderedMarkdown = computed(() => {
  return marked(props.message)
})
</script>

<style scoped>
.message-container {
  display: flex;
  margin-bottom: 16px;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.user-message {
  justify-content: flex-end;
}

.user-bubble {
  background-color: rgb(33, 33, 33);
  color: white;
  border-bottom-right-radius: 4px;
}

.ai-bubble {
  background-color: #F0F0F0;
  color: black;
  border-bottom-left-radius: 4px;
}

.message-content :deep(p) {
  margin: 0;
}

.message-content :deep(ul), .message-content :deep(ol) {
  margin: 8px 0;
  padding-left: 20px;
}

.message-content :deep(li) {
  margin-bottom: 4px;
}

.message-content :deep(code) {
  background-color: rgba(0, 0, 0, 0.1);
  padding: 2px 4px;
  border-radius: 4px;
}
</style>
