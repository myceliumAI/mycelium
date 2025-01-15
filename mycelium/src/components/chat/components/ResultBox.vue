<template>
  <div class="message-container" :class="{ 'user-message': isUser }">
    <div class="message-bubble" :class="isUser ? 'user-bubble' : 'ai-bubble'">
      <div class="message-content" v-html="sanitizedContent"></div>
    </div>
  </div>
</template>

<script setup>
import DOMPurify from 'dompurify'
import { marked } from 'marked'
import { computed } from 'vue'

const props = defineProps({
  message: {
    type: String,
    required: true,
    default: ''
  },
  isUser: {
    type: Boolean,
    default: false
  }
})

// Configure marked options if needed
marked.setOptions({
  gfm: true,  // GitHub Flavored Markdown
  breaks: true,  // Convert \n to <br>
  sanitize: false  // We'll use DOMPurify instead
})

const sanitizedContent = computed(() => {
  if (!props.message) return ''
  
  // First convert markdown to HTML
  const htmlContent = marked(props.message)
  
  // Then sanitize the HTML
  const sanitized = DOMPurify.sanitize(htmlContent, {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'code', 'pre', 'ul', 'ol', 'li', 'a'],
    ALLOWED_ATTR: ['href', 'target', 'rel']
  })
  
  return sanitized
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
  font-family: monospace;
}

.message-content :deep(pre) {
  background-color: rgba(0, 0, 0, 0.1);
  padding: 8px;
  border-radius: 4px;
  overflow-x: auto;
}

.message-content :deep(pre code) {
  background-color: transparent;
  padding: 0;
}

.message-content :deep(a) {
  color: inherit;
  text-decoration: underline;
}
</style>
