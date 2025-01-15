<template>
  <SidePanel title="Data Contracts" @close="$emit('close')">
    <template #header-actions>
      <v-btn
        icon="mdi-refresh"
        variant="text"
        :loading="tableLoading"
        class="mr-2"
        title="Refresh list"
        @click="fetchDataContracts"
      />
      <v-btn
        icon="mdi-delete"
        color="error"
        variant="text"
        :disabled="selectedItems.length === 0"
        :loading="isDeleting"
        :title="`Delete ${selectedItems.length} selected item(s)`"
        @click="handleDelete"
      />
      <v-btn
        icon="mdi-close"
        variant="text"
        class="ml-2"
        @click="$emit('close')"
      />
    </template>

    <v-data-table
      v-model="selectedItems"
      :items="dataContracts"
      :headers="headers"
      :loading="tableLoading"
      show-select
      item-value="id"
      density="comfortable"
    />

    <!-- Confirmation Dialog -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title>Confirm Deletion</v-card-title>
        <v-card-text>
          Are you sure you want to delete {{ selectedItems.length }} selected item(s)?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="showDeleteDialog = false">Cancel</v-btn>
          <v-btn 
            color="error" 
            variant="text" 
            :loading="isDeleting"
            @click="confirmDelete"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </SidePanel>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import SidePanel from '@/components/sidePanel/SidePanel.vue'

const dataContracts = ref([])
const isDeleting = ref(false)
const tableLoading = ref(false)
const showDeleteDialog = ref(false)
const selectedItems = ref([])

const headers = [
  { title: 'Title', key: 'info.title' },
  { title: 'Version', key: 'info.version' },
  { title: 'Description', key: 'info.description' },
  { title: 'Owner', key: 'info.owner' },
  { title: 'Status', key: 'info.status' }
]

const fetchDataContracts = async () => {
  tableLoading.value = true
  try {
    const response = await axios.get('/api/data_contract/')
    if (Array.isArray(response.data.data)) {
      dataContracts.value = response.data.data.map(contract => ({
        id: contract.id,
        info: contract.info
      }))
    } else {
      console.error('💡 Data contracts API did not return a list')
    }
  } catch (error) {
    console.error('❌ Error fetching data contracts:', error)
  } finally {
    tableLoading.value = false
  }
}

const handleDelete = () => {
  if (selectedItems.value.length > 0) {
    showDeleteDialog.value = true
  }
}

const confirmDelete = async () => {
  try {
    isDeleting.value = true
    const deletePromises = selectedItems.value.map(id => {
      console.log('🔍 Deleting contract:', id)
      return axios.delete(`/api/data_contract/${id}`)
    })
    
    await Promise.all(deletePromises)
    console.log('✅ Multiple data contracts deleted successfully')
    selectedItems.value = []
    await fetchDataContracts()
    showDeleteDialog.value = false
  } catch (error) {
    console.error('❌ Error deleting data contract(s):', error)
  } finally {
    isDeleting.value = false
  }
}

onMounted(() => {
  fetchDataContracts()
})

defineEmits(['close'])
</script>
