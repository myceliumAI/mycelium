<template>
  <div class="register-container">
    <v-main class="main-content">
      <v-container fluid class="fill-height">
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="6" lg="4">
            <div class="text-center mb-8">
              <img :src="logoSrc" alt="Mycelium Logo" height="120" />
            </div>
            <v-card class="elevation-12" color="#2f2f2f">
              <v-toolbar color="#212121" dark flat>
                <v-toolbar-title>Register</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form ref="form" v-model="valid" lazy-validation>
                  <v-text-field
                    v-model="name"
                    :rules="nameRules"
                    label="Name"
                    required
                    prepend-icon="mdi-account"
                    color="primary"
                  ></v-text-field>
                  <v-text-field
                    v-model="email"
                    :rules="emailRules"
                    label="Email"
                    required
                    prepend-icon="mdi-email"
                    color="primary"
                  ></v-text-field>
                  <v-text-field
                    v-model="password"
                    :rules="passwordRules"
                    label="Password"
                    required
                    prepend-icon="mdi-lock"
                    type="password"
                    color="primary"
                  ></v-text-field>
                  <v-text-field
                    v-model="confirmPassword"
                    :rules="confirmPasswordRules"
                    label="Confirm Password"
                    required
                    prepend-icon="mdi-lock-check"
                    type="password"
                    color="primary"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-btn color="secondary" @click="goToLogin" text>Login</v-btn>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="register" :disabled="!valid">Register</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </div>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getKeycloak } from '@/services/keycloak'

export default defineComponent({
  name: 'UserRegister',
  setup () {
    const router = useRouter()
    const keycloak = getKeycloak()
    const valid = ref(false)
    const name = ref('')
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const logoSrc = require('@/assets/logo.png')
    const errorMessage = ref('')

    const nameRules = [
      v => !!v || 'Name is required',
      v => (v && v.length <= 50) || 'Name must be less than 50 characters'
    ]

    const emailRules = [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
    ]

    const passwordRules = [
      v => !!v || 'Password is required',
      v => (v && v.length >= 8) || 'Password must be at least 8 characters'
    ]

    const confirmPasswordRules = computed(() => [
      v => !!v || 'Confirm password is required',
      v => v === password.value || 'Passwords must match'
    ])

    const register = async () => {
      if (!valid.value) return

      try {
        await keycloak.register({
          username: email.value,
          firstName: name.value,
          email: email.value,
          password: password.value
        })
        console.log('✅ Registration successful')
        router.push('/login')
      } catch (error) {
        console.error('❌ Registration failed:', error)
        errorMessage.value = 'Registration failed. Please try again.'
      }
    }

    const goToLogin = () => {
      keycloak.login()
    }

    return {
      valid,
      name,
      email,
      password,
      confirmPassword,
      nameRules,
      emailRules,
      passwordRules,
      confirmPasswordRules,
      register,
      logoSrc,
      goToLogin,
      errorMessage
    }
  }
})
</script>

<style scoped>
.register-container {
  height: 100vh;
  display: flex;
  background-color: #2f2f2f;
}

.main-content {
  flex: 1;
  overflow: hidden;
}

:deep(.v-field__input) {
  color: white !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

.error-message {
  color: #ff5252;
  margin-top: 10px;
}
</style>
