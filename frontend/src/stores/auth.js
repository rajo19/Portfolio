import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'));
  const token = ref(localStorage.getItem('token') || null);
  const loading = ref(false);
  const error = ref(null);
  const router = useRouter();

  const isAuthenticated = computed(() => !!token.value);
  const isLoading = computed(() => loading.value);
  const getError = computed(() => error.value);
  const getUser = computed(() => user.value);
  const getToken = computed(() => token.value);

  const login = async (credentials) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await axios.post('/api/auth/login', {
        username: credentials.username,
        password: credentials.password
      });
      
      const { access_token, user: userData } = response.data;
      
      // Update state
      token.value = access_token;
      user.value = userData;
      
      // Store in localStorage if remember me is true
      if (credentials.rememberMe) {
        localStorage.setItem('token', access_token);
        localStorage.setItem('user', JSON.stringify(userData));
      } else {
        // Use sessionStorage for session-only storage
        sessionStorage.setItem('token', access_token);
        sessionStorage.setItem('user', JSON.stringify(userData));
      }
      
      // Set default auth header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      return true;
    } catch (err) {
      console.error('Login failed:', err);
      error.value = err.response?.data?.message || 'Login failed. Please check your credentials.';
      throw error.value;
    } finally {
      loading.value = false;
    }
  };

  const logout = () => {
    // Clear state
    token.value = null;
    user.value = null;
    
    // Clear all auth storage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('user');
    
    // Remove auth header
    delete axios.defaults.headers.common['Authorization'];
    
    // Redirect to home page
    router.push('/login')
  }

  // Initialize function to set auth state
  const init = () => {
    // Check for token in localStorage or sessionStorage
    const storedToken = localStorage.getItem('token') || sessionStorage.getItem('token');
    const storedUser = localStorage.getItem('user') || sessionStorage.getItem('user');
    
    if (storedToken && storedUser) {
      token.value = storedToken;
      user.value = JSON.parse(storedUser);
      axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
    }
  };
  
  // Call init on store creation
  init();
  
  return {
    // State
    user: getUser,
    token: getToken,
    loading: isLoading,
    error: getError,
    
    // Getters
    isAuthenticated,
    isLoading,
    getError,
    getUser,
    
    // Actions
    login,
    logout,
    init
  };
});
