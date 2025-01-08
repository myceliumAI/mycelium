<template>
  <div class="home-container">
    <NavBar
      @new-chat="handleNewChat"
      @create-data-contract="handleCreateDataContract"
      @list-data-contracts="handleListDataContracts"
    />
    <v-main class="main-content">
      <v-container fluid class="pa-0 fill-height">
        <v-row no-gutters class="fill-height" :class="{ 'object-open': isObjectVisible }">
          <v-col :cols="isObjectVisible ? 6 : 12" class="d-flex flex-column">
            <ChatColumn
              ref="chatColumn"
              @request-object="handleObjectRequest"
              @close-object="closeObject"
            />
          </v-col>

          <v-col v-if="isObjectVisible" cols="6" class="d-flex flex-column">
            <component
              :is="currentObjectComponent"
              @close-object="closeObject"
              @contract-added="handleContractAdded"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </div>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import NavBar from '@/components/navigation/NavBar.vue'
import DataContract from '@/components/dataContract/DataContract.vue'
import ListDataContracts from '@/components/listDataContracts/ListDataContracts.vue'
import ChatColumn from '@/components/chat/ChatColumn.vue'

export default defineComponent({
  name: 'HomePage',
  components: {
    NavBar,
    DataContract,
    ListDataContracts,
    ChatColumn
  },
  setup() {
    const isObjectVisible = ref(false)
    const currentObjectComponent = ref(null)
    const chatColumn = ref(null)

    const searchResultsColumnClass = computed(() => ({
      'search-results-column': true,
      'object-open': isObjectVisible.value
    }))

    const handleObjectRequest = (objectType) => {
      isObjectVisible.value = true
      currentObjectComponent.value = objectType
    }

    const closeObject = () => {
      isObjectVisible.value = false
      currentObjectComponent.value = null
    }

    const handleNewChat = () => {
      closeObject()
      chatColumn.value.clearChat()
    }

    const handleCreateDataContract = () => {
      handleObjectRequest('DataContract')
    }

    const handleListDataContracts = () => {
      handleObjectRequest('ListDataContracts')
    }

    const handleContractAdded = () => {
      // If ListDataContracts is currently visible, refresh it
      if (currentObjectComponent.value === 'ListDataContracts') {
        // Assuming ListDataContracts has a method to refresh its data
        this.$refs.listDataContracts.fetchDataContracts()
      }
    }

    return {
      isObjectVisible,
      currentObjectComponent,
      searchResultsColumnClass,
      handleObjectRequest,
      closeObject,
      handleNewChat,
      handleCreateDataContract,
      handleListDataContracts,
      chatColumn,
      handleContractAdded
    }
  }
})
</script>

<style scoped>
.home-container {
  height: 100vh;
  display: flex;
}

.main-content {
  flex: 1;
  overflow: hidden;
}

.object-open .search-results-column {
  text-align: left;
}

.search-results-column {
  text-align: center;
}
</style>
