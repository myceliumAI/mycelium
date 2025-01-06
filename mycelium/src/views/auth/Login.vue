<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-card-title class="text-center">
            <h1 class="text-h5">Login to Mycelium</h1>
          </v-card-title>
          <v-card-text>
            <v-alert
              v-if="error"
              type="error"
              class="mb-4"
            >
              {{ error }}
            </v-alert>

            <v-btn
              color="primary"
              block
              @click="handleLogin"
              :loading="loading"
              class="mt-4"
            >
              Login with Keycloak
            </v-btn>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn
              variant="text"
              to="/register"
              color="primary"
            >
              Create Account
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { authService } from '@/services/auth.service'

export default defineComponent({
  name: 'UserLogin',
  setup() {
    const loading = ref(false)
    const error = ref('')

    const handleLogin = async () => {
      loading.value = true
      error.value = ''

      try {
        await authService.login()
        console.log('✅ Login initiated')
      } catch (err) {
        console.error('❌ Login failed:', err)
        error.value = 'Failed to initialize login. Please try again.'
      } finally {
        loading.value = false
      }
    }

    return {
      loading,
      error,
      handleLogin
    }
  }
})
</script>
