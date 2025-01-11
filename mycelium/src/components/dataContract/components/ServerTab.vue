<template>
  <v-container>
    <DynamicSourceForm
      v-model="sourceConfig"
      @validation="handleValidation"
    />
  </v-container>
</template>

<script>
import { ref, watch } from 'vue'
import DynamicSourceForm from './DynamicSourceForm.vue'

export default {
  name: 'ServerTab',
  components: {
    DynamicSourceForm
  },
  emits: ['update', 'validate'],
  
  setup(props, { emit }) {
    const sourceConfig = ref(null)
    const isValid = ref(false)

    watch(sourceConfig, (newValue) => {
      if (newValue) {
        emit('update', {
          type: newValue.sourceType,
          configuration: newValue.data
        })
      }
    })

    const handleValidation = (valid) => {
      isValid.value = valid
      emit('validate', valid)
    }

    return {
      sourceConfig,
      handleValidation
    }
  }
}
</script>
