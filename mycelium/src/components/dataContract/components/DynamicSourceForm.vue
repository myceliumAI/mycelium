<template>
  <div class="dynamic-form">
    <v-row>
      <v-col
        v-for="field in fields"
        :key="field.name"
        :cols="getFieldColSize(field)"
      >
        <!-- Text & Password fields -->
        <v-text-field
          v-if="field.type === 'text' || field.type === 'password'"
          v-model="formData[field.name]"
          :label="field.label"
          :type="field.type"
          :placeholder="field.placeholder"
          :rules="getFieldRules(field)"
          :required="field.required"
          :hint="field.hint"
          :persistent-hint="!!field.hint"
        />

        <!-- Textarea fields -->
        <v-textarea
          v-else-if="field.type === 'textarea'"
          v-model="formData[field.name]"
          :label="field.label"
          :rules="getFieldRules(field)"
          :required="field.required"
          :hint="field.hint"
          :persistent-hint="!!field.hint"
          :rows="field.rows || 3"
        />

        <!-- Number fields -->
        <v-text-field
          v-else-if="field.type === 'number'"
          v-model.number="formData[field.name]"
          :label="field.label"
          type="number"
          :rules="getFieldRules(field)"
          :required="field.required"
          :hint="field.hint"
          :persistent-hint="!!field.hint"
          :min="field.min"
          :max="field.max"
          :step="field.step || 1"
        />

        <!-- Boolean fields -->
        <v-switch
          v-else-if="field.type === 'boolean'"
          v-model="formData[field.name]"
          :label="field.label"
          :hint="field.hint"
          :persistent-hint="!!field.hint"
          color="primary"
        />

        <!-- Select fields -->
        <v-select
          v-else-if="field.type === 'select'"
          v-model="formData[field.name]"
          :items="field.options"
          :label="field.label"
          :rules="getFieldRules(field)"
          :required="field.required"
          :hint="field.hint"
          :persistent-hint="!!field.hint"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  fields: {
    type: Array,
    required: true
  },
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'validation'])

const formData = ref({})
const valid = ref(true)

// Initialize form data
watch(() => props.fields, (newFields) => {
  // Initialize form data with default values for new fields
  newFields.forEach(field => {
    if (!(field.name in formData.value)) {
      formData.value[field.name] = field.default !== undefined ? field.default : 
        field.type === 'boolean' ? false :
        field.type === 'number' ? null :
        ''
    }
  })
}, { immediate: true })

// Watch for changes in form data
watch(formData, (newValue) => {
  emit('update:modelValue', newValue)
  validateForm()
}, { deep: true })

const getFieldColSize = (field) => {
  if (field.type === 'textarea') return 12
  if (field.type === 'boolean') return 12
  return 6
}

const getFieldRules = (field) => {
  const rules = []

  if (field.required) {
    rules.push(v => !!v || `${field.label} is required`)
  }

  if (field.pattern) {
    rules.push(v => new RegExp(field.pattern).test(v) || field.patternError || 'Invalid format')
  }

  if (field.type === 'number') {
    if (field.min !== undefined) {
      rules.push(v => v >= field.min || `Minimum value is ${field.min}`)
    }
    if (field.max !== undefined) {
      rules.push(v => v <= field.max || `Maximum value is ${field.max}`)
    }
  }

  return rules
}

const validateForm = () => {
  const isValid = props.fields.every(field => {
    if (field.required) {
      return !!formData.value[field.name]
    }
    return true
  })
  valid.value = isValid
  emit('validation', isValid)
}
</script>

<style scoped>
.dynamic-form {
  padding: 16px;
}
</style> 