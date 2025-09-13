<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useTheme } from 'vuetify';
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import { mdiAccountCog, mdiBriefcase, mdiEmail, mdiFileDocument, mdiHome, mdiLogout, mdiPost, mdiRobot, mdiStar } from '@mdi/js';

const theme = useTheme({ defaultTheme: 'light' });
const route = useRoute();
const authStore = useAuthStore();
const drawer = ref(false);
const isMobile = ref(window.innerWidth < 960);
const profilePictureUrl = ref('');

// Load profile picture with timestamp to prevent caching
const loadProfilePicture = async () => {
  try {
    // Add timestamp to prevent caching
    const timestamp = new Date().getTime();
    const response = await axios.get(`/api/profile/profile_pic?t=${timestamp}`, {
      responseType: 'blob',
      validateStatus: status => status < 500 // Don't throw for 404
    });
    
    if (response.status === 200 && response.data) {
      // Create a blob URL from the response
      const blob = new Blob([response.data], { type: response.data.type || 'image/jpeg' });
      profilePictureUrl.value = URL.createObjectURL(blob);
    } else if (response.status === 404) {
      console.log('No profile picture found');
      profilePictureUrl.value = '';
    }
  } catch (error) {
    console.error('Error loading profile picture:', error);
    profilePictureUrl.value = '';
  }
};

// Load profile picture on mount
onMounted(() => {
  loadProfilePicture();
  window.addEventListener('resize', handleResize);
  
  // Close drawer on mobile when route changes
  if (isMobile.value) {
    drawer.value = false;
  }
});

// Navigation items
const navItems = [
  { title: 'Home', to: '/' , icon: mdiHome},
  { title: 'Portfolio', to: '/portfolio' , icon: mdiBriefcase},
  { title: 'CV', to: '/cv' , icon: mdiFileDocument},
  { title: 'Blog', to: '/blog' , icon: mdiPost},
  { title: 'Contact', to: '/contact' , icon: mdiEmail},
  { title: 'About', to: '/about' , icon: mdiAccountCog},
  { title: 'AI Assistant', to: '/ai' , icon: mdiRobot},
];

// Social media links
const socialIcons = [
  { icon: 'mdi-github', link: 'https://github.com/rajorshi' },
  { icon: 'mdi-linkedin', link: 'https://linkedin.com/in/rajorshi-tah' },
  { icon: 'mdi-twitter', link: 'https://twitter.com/rajorshitah' },
];

// Check if current route is active
const isActive = (path) => {
  return route.path === path || (path !== '/' && route.path.startsWith(path));
};

// Handle window resize
const handleResize = () => {
  isMobile.value = window.innerWidth < 960;
  if (!isMobile.value) {
    drawer.value = false;
  }
};
</script>

<template>
  <v-app :theme="theme.global.name.value">
    <!-- Enhanced App Bar -->
    <v-app-bar 
      app 
      :elevation="4"
      color="accent"
      class="px-4"
    >
      <!-- Mobile Menu Button -->
      <v-app-bar-nav-icon 
        @click="drawer = !drawer" 
        variant="text"
        size="small"
      />
      
      <!-- Logo/Brand -->
      <v-toolbar-title class="font-weight-bold ml-2">
        <router-link to="/" class="brand-link text-decoration-none d-flex align-center">
          <div class="d-flex flex-column">
            <span class="text-h5 font-weight-black text-gradient">RAJORSHI</span>
          </div>
        </router-link>
      </v-toolbar-title>
      
      <v-spacer />
      
      <!-- Desktop Navigation -->
      <v-toolbar-items class="d-none d-lg-flex align-center">
        <v-btn
          v-for="item in navItems"
          :key="item.title"
          :to="item.to"
          variant="text"
          :active="isActive(item.to)"
          class="text-none mx-1"
          :class="{
            'text-none mx-1': isActive(item.to),
            'text-medium-emphasis': !isActive(item.to)
          }"
          rounded="lg"
          height="48"
        >
          {{ item.title }}
        </v-btn>
        
        <!-- Profile Button with Avatar -->
        <v-menu offset-y>
          <template v-slot:activator="{ props: menuProps }">
            <v-btn
              v-bind="menuProps"
              class="mx-1"
              variant="text"
              height="48"
              min-width="auto"
              :ripple="false"
            >
              <v-avatar size="36" class="mr-1">
                <v-img
                  v-if="profilePictureUrl"
                  :src="profilePictureUrl"
                  alt="Profile"
                  cover
                >
                  <template v-slot:placeholder>
                    <v-icon>mdi-account</v-icon>
                  </template>
                </v-img>
                <v-icon v-else>mdi-account</v-icon>
              </v-avatar>
            </v-btn>
          </template>
          
          <v-list density="comfortable" class="py-1" min-width="100">
            <v-list-item
              v-for="(item, i) in [
                { 
                  title: 'Profile', 
                  icon: mdiAccountCog, 
                  to: '/profile-management',
                  color: 'primary'
                },
                { 
                  title: 'Logout', 
                  icon: mdiLogout, 
                  action: 'logout',
                  color: 'error'
                }
              ]"
              :key="i"
              :value="i"
              @click="item.action === 'logout' ? authStore.logout() : null"
              :to="item.action === 'logout' ? null : item.to"
              :ripple="false"
              link
              class="px-3 py-1 menu-item"
              :class="{ 'text-error': item.action === 'logout' }"
              :active="false"
            >
              <template v-slot:prepend>
                <v-icon 
                  :icon="item.icon" 
                  size="small" 
                  class="mr-3"
                  :color="item.color"
                />
              </template>
              <v-list-item-title 
                class="text-body-2 font-weight-medium"
                :class="{ 'text-error': item.action === 'logout' }"
              >
                {{ item.title }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        
        <v-btn
          v-if="!authStore.isAuthenticated"
          to="/login"
          class="mx-1 text-none login-button"
          color="login"
          variant="flat"
          elevation="2"
        >
          Login
        </v-btn>
        
      </v-toolbar-items>
    </v-app-bar>

    <!-- Enhanced Mobile Navigation Drawer -->
    <v-navigation-drawer 
      v-model="drawer" 
      app 
      temporary
      location="left"
      width="300"
      class="px-2"
    >
      <v-list>
        <v-list-item class="mb-4">
          <template v-slot:prepend>
            <v-avatar size="48" class="mr-3">
              <v-img
                v-if="profilePictureUrl"
                :src="profilePictureUrl"
                alt="Profile"
                cover
              >
                <template v-slot:placeholder>
                  <v-icon>mdi-account</v-icon>
                </template>
              </v-img>
              <v-icon v-else>mdi-account</v-icon>
            </v-avatar>
          </template>
          <v-list-item-title class="text-h6 font-weight-bold">Rajorshi Tah</v-list-item-title>
          <v-list-item-subtitle>Full Stack Developer</v-list-item-subtitle>
        </v-list-item>
        
        <v-divider class="mb-4" />
        
        <v-list-item
          v-for="item in navItems"
          :key="item.title"
          :to="item.to"
          :prepend-icon="item.icon"
          :title="item.title"
          :active="isActive(item.to)"
          @click="drawer = false"
          rounded="lg"
          class="mb-2"
          :class="{ 'bg-primary text-white': isActive(item.to) }"
        >
          <template v-slot:prepend>
            <v-icon :color="isActive(item.to) ? 'white' : 'login'">{{ item.icon }}</v-icon>
          </template>
        </v-list-item>
      </v-list>
      
      <v-spacer />
      
      <div class="pa-4">
        <v-divider class="mb-4" />
        <div class="d-flex justify-center gap-4 mb-4">
          <v-btn
            v-for="icon in socialIcons"
            :key="icon.icon"
            :icon="icon.icon"
            :href="icon.link"
            target="_blank"
            rel="noopener"
            variant="text"
            size="small"
            color="primary"
          />
        </div>
        
        <v-divider class="mb-4" />
        
        <div class="text-center">
          <div class="text-caption text-medium-emphasis">
            {{ new Date().getFullYear() }} Rajorshi Tah
          </div>
          <div class="text-caption text-medium-emphasis">
            Made with <v-icon color="red" size="small">mdi-heart</v-icon> in Tokyo
          </div>
        </div>
      </div>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <v-container fluid class="pa-0 fill-height">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer app inset class="d-none d-lg-block">
      <v-row no-gutters justify="center">
        <v-col cols="12" class="text-center">
          <v-btn
            v-for="icon in socialIcons"
            :key="icon.icon"
            :icon="icon.icon"
            :href="icon.link"
            target="_blank"
            rel="noopener"
            variant="text"
            size="small"
            class="mx-2"
          />
          <div class="text-caption mt-2">
            {{ new Date().getFullYear() }} Rajorshi Tah | All rights reserved
          </div>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<style scoped>
/* Profile Menu */
.menu-item {
  border-radius: 8px;
  margin: 0 8px;
  transition: all 0.2s ease-in-out;
}

.menu-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.08);
}

.menu-item:active {
  transform: translateY(1px);
}

/* Auth Buttons */
.login-button,
.logout-button {
  border-radius: 4px !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
  transition: all 0.3s ease !important;
  height: 40px !important;
  min-width: 90px !important;
  align-self: center;
  margin: 0 4px !important;
}

.login-button:hover,
.logout-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
}

/* Navbar height */
:deep(.v-toolbar) {
  min-height: 64px !important;
  padding: 0 12px !important;
}

/* Brand Styling */
.brand-link {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.brand-link:hover {
  transform: translateY(-1px);
}

.text-gradient {
  background: linear-gradient(45deg, #0d47a1, #1565c0);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 0.05em;
  text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

/* Smooth transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
}

::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* Dark theme scrollbar */
.v-theme--dark ::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

.v-theme--dark ::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
}

.v-theme--dark ::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Custom link styles */
a {
  color: inherit;
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: var(--v-primary-base);
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Custom animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}
</style>
