<template>
  <div class="dynamic-form">
    <v-row>
      <v-col
        v-for="field in fields"
        :key="field.name"
        :cols="getFieldColSize(field)"
      >
        <!-- Arrays -->
        <template v-if="field.type === 'array'">
          <div class="array-field">
            <div class="d-flex align-center mb-2">
              <h3 class="text-h6">{{ field.label }}</h3>
              <v-spacer></v-spacer>
              <v-btn
                icon="mdi-plus"
                size="small"
                color="primary"
                @click="addArrayItem(field.name)"
                :title="`Add ${field.label}`"
              />
            </div>
            
            <div v-if="field.hint" class="text-caption mb-4">{{ field.hint }}</div>

            <v-expansion-panels>
              <v-expansion-panel
                v-for="(item, index) in getArrayValue(field.name)"
                :key="index"
              >
                <v-expansion-panel-title>
                  {{ getArrayItemTitle(field, item, index) }}
                  <template #actions>
                    <v-btn
                      icon="mdi-delete"
                      size="small"
                      color="error"
                      variant="text"
                      @click.stop="removeArrayItem(field.name, index)"
                      :title="`Remove item ${index + 1}`"
                    />
                  </template>
                </v-expansion-panel-title>
                
                <v-expansion-panel-text>
                  <v-row>
                    <v-col
                      v-for="prop in field.items.properties"
                      :key="prop.name"
                      :cols="getPropertyColSize(prop)"
                    >
                      <!-- Nested array -->
                      <template v-if="prop.type === 'array'">
                        <div class="nested-array-field">
                          <div class="d-flex align-center mb-2">
                            <h4 class="text-subtitle-1">{{ prop.label }}</h4>
                            <v-spacer></v-spacer>
                            <v-btn
                              icon="mdi-plus"
                              size="small"
                              color="primary"
                              @click="addNestedArrayItem(field.name, index, prop.name)"
                              :title="`Add ${prop.label}`"
                            />
                          </div>
                          
                          <div v-if="prop.hint" class="text-caption mb-4">{{ prop.hint }}</div>

                          <v-card
                            v-for="(nestedItem, nestedIndex) in getNestedArrayValue(field.name, index, prop.name)"
                            :key="nestedIndex"
                            class="mb-2"
                            variant="outlined"
                          >
                            <v-card-text>
                              <v-row>
                                <v-col
                                  v-for="nestedProp in prop.items.properties"
                                  :key="nestedProp.name"
                                  :cols="getPropertyColSize(nestedProp)"
                                >
                                  <component
                                    :is="getFieldComponent(nestedProp.type)"
                                    v-model="nestedItem[nestedProp.name]"
                                    :label="nestedProp.label"
                                    v-bind="getFieldProps(nestedProp)"
                                  />
                                </v-col>
                              </v-row>
                            </v-card-text>
                            <v-card-actions>
                              <v-spacer></v-spacer>
                              <v-btn
                                icon="mdi-delete"
                                size="small"
                                color="error"
                                variant="text"
                                @click="removeNestedArrayItem(field.name, index, prop.name, nestedIndex)"
                                :title="'Remove item'"
                              />
                            </v-card-actions>
                          </v-card>
                        </div>
                      </template>

                      <!-- Regular field -->
                      <component
                        v-else
                        :is="getFieldComponent(prop.type)"
                        v-model="item[prop.name]"
                        :label="prop.label"
                        v-bind="getFieldProps(prop)"
                      />
                    </v-col>
                  </v-row>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>
        </template>

        <!-- Regular fields (unchanged) -->
        <component
          v-else
          :is="getFieldComponent(field.type)"
          v-model="formData[field.name]"
          :label="field.label"
          v-bind="getFieldProps(field)"
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
  newFields.forEach(field => {
    if (!(field.name in formData.value)) {
      formData.value[field.name] = field.type === 'array' ? [] : 
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

const getFieldComponent = (type) => {
  switch (type) {
    case 'textarea': return 'v-textarea'
    case 'select': return 'v-select'
    case 'boolean': return 'v-switch'
    default: return 'v-text-field'
  }
}

const getFieldProps = (field) => {
  const props = {
    required: field.required,
    hint: field.hint,
    'persistent-hint': !!field.hint,
    placeholder: field.placeholder,
    rules: getFieldRules(field)
  }

  if (field.type === 'select') {
    props.items = field.options
  }

  if (field.type === 'number') {
    props.type = 'number'
    props.min = field.min
    props.max = field.max
    props.step = field.step || 1
  }

  return props
}

const getFieldColSize = (field) => {
  if (field.type === 'array') return 12
  if (field.type === 'textarea') return 12
  if (field.type === 'boolean') return 12
  return 6
}

const getPropertyColSize = (prop) => {
  if (prop.type === 'array') return 12
  if (prop.type === 'textarea') return 12
  return 6
}

const getArrayValue = (fieldName) => {
  if (!formData.value[fieldName]) {
    formData.value[fieldName] = []
  }
  return formData.value[fieldName]
}

const getNestedArrayValue = (fieldName, index, propName) => {
  const array = getArrayValue(fieldName)
  if (!array[index][propName]) {
    array[index][propName] = []
  }
  return array[index][propName]
}

const addArrayItem = (fieldName) => {
  formData.value[fieldName].push({})
}

const removeArrayItem = (fieldName, index) => {
  formData.value[fieldName].splice(index, 1)
}

const addNestedArrayItem = (fieldName, index, propName) => {
  const array = getArrayValue(fieldName)
  if (!array[index][propName]) {
    array[index][propName] = []
  }
  array[index][propName].push({})
}

const removeNestedArrayItem = (fieldName, index, propName, nestedIndex) => {
  formData.value[fieldName][index][propName].splice(nestedIndex, 1)
}

const getArrayItemTitle = (field, item, index) => {
  // Try to find a meaningful title from the item's properties
  const titleField = field.items.properties.find(p => 
    ['name', 'title', 'source_table', 'target_table'].includes(p.name)
  )
  return titleField && item[titleField.name] 
    ? item[titleField.name]
    : `${field.label} ${index + 1}`
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
      if (field.type === 'array') {
        return formData.value[field.name]?.length > 0
      }
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

.array-field {
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 16px;
}

.nested-array-field {
  margin-top: 8px;
  margin-bottom: 8px;
}
</style> 