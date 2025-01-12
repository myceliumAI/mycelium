<template>
  <div class="chat-layout">
    <div class="chat-messages">
      <ResultsList 
        ref="resultsList"
        :messages="messages"
        :is-waiting="isWaitingResponse"
      />
    </div>
    <div class="chat-input">
      <SearchBar 
        ref="searchBar" 
        @search="handleSearch" 
        :disabled="isWaitingResponse" 
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SearchBar from './components/SearchBar.vue'
import ResultsList from './components/ResultsList.vue'

const emit = defineEmits(['requestObject', 'closeObject'])

const messages = ref([])
const resultsList = ref(null)
const searchBar = ref(null)
const isWaitingResponse = ref(false)

const getHelpMessage = () => {
  return `Here are the available commands:
* 🆕 **new**: Create a new Data Contract
* 📋 **list**: Display all Data Contracts
* 🚪 **close**: Close the current object
* ❓ **help**: Display this help message`.trim()
}

const handleSearch = async (search) => {
  if (isWaitingResponse.value) return

  // Add user message
  messages.value.push({ message: search, isUser: true })
  isWaitingResponse.value = true

  // Simulate AI response delay
  await new Promise(resolve => setTimeout(resolve, 1000))

  const lowerCaseSearch = search.toLowerCase()
  let aiResponse = ''

  switch (lowerCaseSearch) {
    case 'new':
      emit('requestObject', 'DataContract')
      aiResponse = '✨ Creating a new Data Contract. What would you like to add?'
      break
    case 'list':
      emit('requestObject', 'ListDataContracts')
      aiResponse = '📋 Displaying the list of Data Contracts.'
      break
    case 'close':
      emit('closeObject')
      aiResponse = '🚪 Closing the current object.'
      break
    case 'help':
      aiResponse = getHelpMessage()
      break
    default:
      aiResponse = `❓ I'm sorry, I don't understand "${search}".\n\n${getHelpMessage()}`
  }

  // Add AI response
  messages.value.push({ message: aiResponse, isUser: false })
  isWaitingResponse.value = false

  // Refocus the input
  searchBar.value?.focusInput()
}

const clearChat = () => {
  messages.value = []
}

defineExpose({ clearChat })
</script>

<style scoped>
.chat-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.chat-input {
  padding: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.12);
  background-color: var(--v-surface-variant);
}
</style>
