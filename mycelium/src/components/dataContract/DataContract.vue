<template>
  <SidePanel title="Create Data Contract" @close="$emit('close')">
    <!-- Template Selection -->
    <v-select
      v-model="selectedTemplate"
      :items="availableTemplates"
      label="Select Template"
      item-title="name"
      item-value="id"
      :loading="loadingTemplates"
      :disabled="loadingTemplates"
      @update:model-value="loadTemplate"
      class="mb-4"
    >
      <template v-slot:prepend-item>
        <v-list-item>
          <v-list-item-title class="text-caption text-grey">
            Select a template to start creating your data contract
          </v-list-item-title>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
    </v-select>

    <!-- Dynamic Form -->
    <template v-if="selectedTemplate && templateData">
      <v-tabs v-model="tab" background-color="primary">
        <v-tab
          v-for="(tabContent, tabKey) in templateData.tabs"
          :key="tabKey"
          :value="tabKey"
        >
          {{ tabContent.label }}
        </v-tab>
      </v-tabs>

      <v-window v-model="tab">
        <v-window-item
          v-for="(tabContent, tabKey) in templateData.tabs"
          :key="tabKey"
          :value="tabKey"
        >
          <v-card flat>
            <v-card-text>
              <div class="text-subtitle-1 mb-4">{{ tabContent.description }}</div>
              <DynamicSourceForm
                :fields="tabContent.fields"
                v-model="formData[tabKey]"
                @validation="handleValidation"
              />
            </v-card-text>
          </v-card>
        </v-window-item>
      </v-window>
    </template>

    <template #footer>
      <v-btn
        color="primary"
        @click="submitObject"
        :loading="isSubmitting"
        :disabled="!isValid || !selectedTemplate"
      >
        Create Contract
      </v-btn>
    </template>

    <!-- Success/Error Snackbar -->
    <v-snackbar
      v-model="showSnackbar"
      :color="snackbarColor"
      :timeout="3000"
    >
      {{ snackbarText }}
    </v-snackbar>
  </SidePanel>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import SidePanel from '@/components/sidePanel/SidePanel.vue'
import DynamicSourceForm from './components/DynamicSourceForm.vue'

const emit = defineEmits(['close', 'contract-added'])

// Form state
const tab = ref(null)
const selectedTemplate = ref(null)
const templateData = ref(null)
const formData = ref({})
const isValid = ref(false)
const loadingTemplates = ref(true)
const availableTemplates = ref([])
const isSubmitting = ref(false)
const showSnackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

// Load available templates
const loadAvailableTemplates = async () => {
  try {
    loadingTemplates.value = true
    console.log('🔍 Fetching templates...')
    const response = await axios.get('/api/template/')
    console.log('✅ Templates loaded:', response.data)
    availableTemplates.value = response.data.templates
  } catch (error) {
    console.error('❌ Error loading templates:', error)
    showMessage('Error loading templates', 'error')
  } finally {
    loadingTemplates.value = false
  }
}

// Load specific template
const loadTemplate = async (templateId) => {
  try {
    console.log('🔍 Loading template:', templateId)
    const response = await axios.get(`/api/template/${templateId}`)
    templateData.value = response.data
    formData.value = {}
    
    // Initialize form data for each tab
    Object.keys(templateData.value.tabs).forEach(tabKey => {
      formData.value[tabKey] = {}
    })
    
    // Set first tab as active
    tab.value = Object.keys(templateData.value.tabs)[0]
    console.log('✅ Template loaded successfully')
  } catch (error) {
    console.error('❌ Error loading template:', error)
    showMessage('Error loading template', 'error')
  }
}

const handleValidation = (valid) => {
  isValid.value = valid
}

const showMessage = (text, color = 'success') => {
  snackbarText.value = text
  snackbarColor.value = color
  showSnackbar.value = true
}

const submitObject = async () => {
  try {
    isSubmitting.value = true
    // Merge data from all tabs
    const mergedData = {
      template: selectedTemplate.value,
      ...Object.values(formData.value).reduce((acc, curr) => ({ ...acc, ...curr }), {})
    }
    
    const response = await axios.post('/api/data_contract/', mergedData)
    console.log('✅ Data contract submitted successfully:', response.data)
    showMessage('Data contract created successfully')
    emit('contract-added', response.data)
    emit('close')
  } catch (error) {
    console.error('❌ Error submitting data contract:', error)
    showMessage('Error creating data contract', 'error')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  loadAvailableTemplates()
})
</script>

<style scoped>
.v-window {
  overflow-y: auto;
  max-height: calc(100vh - 300px);
}

.v-window-item {
  height: 100%;
  overflow-y: auto;
}
</style>