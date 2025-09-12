<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useDisplay } from 'vuetify';
import { useAuthStore } from '@/stores/auth';

const { mobile } = useDisplay();
const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const form = ref({
  username: '',
  password: '',
  rememberMe: false
});

const isFormValid = ref(false);
const loading = ref(false);
const showPassword = ref(false);
const snackbar = ref({
  show: false,
  message: '',
  color: 'error'
});

// Validation rules
const usernameRules = [
  v => !!v || 'Username is required',
  v => (v && v.length >= 3) || 'Username must be at least 3 characters'
];

const passwordRules = [
  v => !!v || 'Password is required',
  v => (v && v.length >= 6) || 'Password must be at least 6 characters'
];

const login = async () => {
  if (!isFormValid.value) return;
  
  loading.value = true;
  
  try {
    await authStore.login({
      username: form.value.username,
      password: form.value.password,
      remember: form.value.rememberMe
    });
    
    // Redirect to intended route or dashboard
    const redirectTo = route.query.redirect || '/';
    await router.push(redirectTo);
    
    snackbar.value = {
      show: true,
      message: 'Login successful! Welcome back.',
      color: 'success'
    };
  } catch (error) {
    console.error('Login error:', error);
    
    snackbar.value = {
      show: true,
      message: error.response?.data?.message || 'Invalid credentials. Please try again.',
      color: 'error'
    };
  } finally {
    loading.value = false;
  }
};

// Clear form
const clearForm = () => {
  form.value = {
    username: '',
    password: '',
    rememberMe: false
  };
  isFormValid.value = false;
};
</script>

<template>
  <VContainer class="login-container py-8">
    <VRow justify="center" align="center" class="min-h-screen">
      <VCol cols="12" sm="8" md="6" lg="4" xl="3">
        <VCard class="pa-8 elevation-8" rounded="lg">
          <!-- Header -->
          <div class="text-center mb-8">
            <VIcon size="64" color="primary" class="mb-4">mdi-account-circle</VIcon>
            <h1 class="text-h4 font-weight-bold mb-2">Welcome Back</h1>
            <p class="text-body-2 text-medium-emphasis">
              Sign in to access your admin dashboard
            </p>
          </div>
          
          <!-- Login Form -->
          <VForm @submit.prevent="login" v-model="isFormValid">
            <VTextField
              v-model="form.username"
              label="Username"
              :rules="usernameRules"
              required
              variant="outlined"
              class="mb-4"
              prepend-inner-icon="mdi-account"
              :disabled="loading"
              autocomplete="username"
            />
            
            <VTextField
              v-model="form.password"
              label="Password"
              :rules="passwordRules"
              required
              variant="outlined"
              :type="showPassword ? 'text' : 'password'"
              class="mb-4"
              prepend-inner-icon="mdi-lock"
              :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showPassword = !showPassword"
              :disabled="loading"
              autocomplete="current-password"
            />
            
            <div class="d-flex justify-space-between align-center mb-6">
              <VCheckbox
                v-model="form.rememberMe"
                label="Remember me"
                hide-details
                density="comfortable"
                :disabled="loading"
              />
              
              <VBtn
                variant="text"
                size="small"
                color="primary"
                class="text-caption"
                @click="() => {}"
              >
                Forgot password?
              </VBtn>
            </div>
            
            <VBtn
              type="submit"
              color="primary"
              size="large"
              block
              :loading="loading"
              :disabled="!isFormValid || loading"
              class="mb-6"
              rounded
            >
              <VIcon start v-if="!loading">mdi-login</VIcon>
              {{ loading ? 'Signing in...' : 'Sign In' }}
            </VBtn>
            
            <!-- Demo Credentials -->
            <VAlert
              type="info"
              variant="tonal"
              class="mb-4"
              density="compact"
            >
              <div class="text-caption">
                <strong>Demo Credentials:</strong><br>
                Username: admin<br>
                Password: password123
              </div>
            </VAlert>
            
            <!-- Clear Form -->
            <div class="text-center">
              <VBtn
                variant="text"
                size="small"
                @click="clearForm"
                :disabled="loading"
              >
                Clear Form
              </VBtn>
            </div>
          </VForm>
        </VCard>
      </VCol>
    </VRow>
    
    <!-- Snackbar for notifications -->
    <VSnackbar 
      v-model="snackbar.show" 
      :color="snackbar.color" 
      timeout="4000"
      location="top"
    >
      {{ snackbar.message }}
      
      <template v-slot:actions>
        <VBtn
          variant="text"
          @click="snackbar.show = false"
        >
          Close
        </VBtn>
      </template>
    </VSnackbar>
  </VContainer>
</template>

<style scoped>
.login-container {
  max-width: 100%;
  min-height: 100vh;
}

.min-h-screen {
  min-height: 100vh;
}

.v-card {
  border-radius: 16px !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
}

.v-btn {
  text-transform: none;
  letter-spacing: normal;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .v-card {
    margin: 16px;
  }
  
  h1 {
    font-size: 1.75rem !important;
  }
}
</style>
