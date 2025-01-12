<template>
  <div class="results-list" ref="messagesContainer">
    <v-container>
      <v-row>
        <v-col cols="12" v-for="(message, index) in messages" :key="index">
          <ResultBox 
            :message="message.message" 
            :is-user="message.isUser" 
          />
        </v-col>
      </v-row>
      <v-row v-if="isWaiting">
        <v-col cols="12">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import ResultBox from './ResultBox.vue'

const props = defineProps({
  messages: {
    type: Array,
    required: true,
    default: () => []
  },
  isWaiting: {
    type: Boolean,
    default: false
  }
})

const messagesContainer = ref(null)

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Watch for changes in messages or waiting state
watch(
  [() => props.messages, () => props.isWaiting],
  () => {
    nextTick(scrollToBottom)
  },
  { deep: true }
)
</script>

<style scoped>
.results-list {
  height: 100%;
  overflow-y: auto;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 8px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background-color: var(--v-medium-emphasis-opacity);
  border-radius: 50%;
  animation: bounce 1s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}
</style>
