<template>
  <div class="search-bar">
    <v-form @submit.prevent="handleSubmit">
      <v-text-field
        ref="searchInput"
        v-model="inputValue"
        append-inner-icon="mdi-send"
        variant="outlined"
        placeholder="Type a command or 'help' for available options..."
        clearable
        hide-details
        density="comfortable"
        :disabled="disabled"
        @keyup.enter="handleSubmit"
        @click:append-inner="handleSubmit"
      />
    </v-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['search'])

const inputValue = ref('')
const searchInput = ref(null)

const handleSubmit = () => {
  if (inputValue.value.trim() === '' || props.disabled) return
  
  emit('search', inputValue.value.trim())
  inputValue.value = ''
}

const focusInput = () => {
  searchInput.value?.focus()
}

defineExpose({ focusInput })
</script>

<style scoped>
.search-bar {
  width: 100%;
}

.v-form {
  padding: 0;
}

.v-text-field {
  margin: 0;
}
</style>
