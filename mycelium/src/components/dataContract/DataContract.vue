<template>
  <v-card class="scrollable-card">
    <div class="close-button-container">
      <CloseButton @close="closeObject" />
    </div>
    
    <v-card-title class="d-flex align-center">
      <span>Data Contract</span>
    </v-card-title>

    <!-- Template Selection -->
    <v-card-text>
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
    </v-card-text>

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

    <v-card-actions class="submit-button-container">
      <SubmitButton 
        @submitObject="submitObject" 
        :isDisabled="!isValid || !selectedTemplate"
      />
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import CloseButton from './components/CloseButton.vue'
import DynamicSourceForm from './components/DynamicSourceForm.vue'
import SubmitButton from './components/SubmitButton.vue'
import { useResizeObserver } from '@/composables/useResizeObserver'

const emit = defineEmits(['close-object', 'contract-added'])

const tab = ref(null)
const selectedTemplate = ref(null)
const templateData = ref(null)
const formData = ref({})
const isValid = ref(false)
const loadingTemplates = ref(true)
const availableTemplates = ref([])

// Charger la liste des templates disponibles
const loadAvailableTemplates = async () => {
  try {
    loadingTemplates.value = true
    console.log('Fetching templates...')
    const response = await axios.get('/api/template/templates')
    console.log('Templates response:', response.data)
    availableTemplates.value = response.data.templates
  } catch (error) {
    console.error('Error loading templates:', error)
  } finally {
    loadingTemplates.value = false
  }
}

// Charger un template spécifique
const loadTemplate = async (templateId) => {
  try {
    const response = await axios.get(`/api/template/templates/${templateId}`)
    templateData.value = response.data
    formData.value = {}
    
    // Initialiser les données du formulaire pour chaque onglet
    Object.keys(templateData.value.tabs).forEach(tabKey => {
      formData.value[tabKey] = {}
    })
    
    // Définir le premier onglet comme actif
    tab.value = Object.keys(templateData.value.tabs)[0]
  } catch (error) {
    console.error('Error loading template:', error)
  }
}

const handleValidation = (valid) => {
  isValid.value = valid
}

const submitObject = async () => {
  try {
    // Fusionner les données de tous les onglets
    const mergedData = {
      template: selectedTemplate.value,
      ...Object.values(formData.value).reduce((acc, curr) => ({ ...acc, ...curr }), {})
    }
    
    const response = await axios.post('/api/data_contract/', mergedData)
    console.log('Data contract submitted successfully:', response.data)
    emit('contract-added')
    emit('close-object')
  } catch (error) {
    console.error('Error submitting data contract:', error)
  }
}

const closeObject = () => {
  emit('close-object')
}

onMounted(() => {
  loadAvailableTemplates()
})

useResizeObserver('.v-window-item')
</script>

<style scoped>
.scrollable-card {
  max-height: calc(100vh - 64px);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  position: relative;
}

.close-button-container {
  position: sticky;
  top: 0;
  right: 0;
  z-index: 1;
  display: flex;
  justify-content: flex-end;
  padding: 8px;
}

.submit-button-container {
  display: flex;
  justify-content: center;
  padding: 5px 0;
}
</style>
