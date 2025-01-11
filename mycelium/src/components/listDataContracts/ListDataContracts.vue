<template>
  <v-card class="position-relative">
    <CloseButton @close-object="handleCloseObject" />
    <v-card-title class="d-flex align-center">
      Data Contracts List
      <v-spacer></v-spacer>
      <v-btn
        icon="mdi-refresh"
        variant="text"
        :loading="tableLoading"
        @click="fetchDataContracts"
        class="mr-2"
        title="Refresh list"
      />
      <v-btn
        icon="mdi-delete"
        color="error"
        variant="text"
        :disabled="selectedItems.length === 0"
        @click="handleDelete"
        :loading="isDeleting"
        :title="`Delete ${selectedItems.length} selected item(s)`"
      />
    </v-card-title>
    <v-card-text>
      <v-data-table
        v-model="selectedItems"
        :items="dataContracts"
        :headers="headers"
        :loading="tableLoading"
        show-select
        item-value="id"
      />
    </v-card-text>

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
            @click="confirmDelete"
            :loading="isDeleting"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import axios from 'axios'
import CloseButton from './components/CloseButton.vue'

export default defineComponent({
  name: 'ListDataContracts',
  components: {
    CloseButton
  },
  emits: ['close-object'],
  setup (props, { emit }) {
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

    const handleCloseObject = () => {
      emit('close-object')
    }

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

    return {
      dataContracts,
      headers,
      handleCloseObject,
      fetchDataContracts,
      handleDelete,
      confirmDelete,
      isDeleting,
      tableLoading,
      showDeleteDialog,
      selectedItems,
    }
  }
})
</script>

<style scoped>
.v-card {
  margin-top: 20px;
  padding: 20px;
}
</style>
