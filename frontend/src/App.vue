<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useTheme } from 'vuetify';
import { useAuthStore } from '@/stores/auth';

const theme = useTheme();
const route = useRoute();
const authStore = useAuthStore();
const drawer = ref(false);
const isMobile = ref(window.innerWidth < 960);

// Navigation items
const navItems = [
  { title: 'Home', to: '/', icon: 'mdi-home' },
  { title: 'Portfolio', to: '/portfolio', icon: 'mdi-briefcase' },
  { title: 'CV', to: '/cv', icon: 'mdi-file-account' },
  { title: 'AI Assistant', to: '/ai', icon: 'mdi-robot' },
  { title: 'Blog', to: '/blog', icon: 'mdi-post' },
  { title: 'Contact', to: '/contact', icon: 'mdi-email' },
  { title: 'About', to: '/about', icon: 'mdi-information' },
];

// Social media links
const socialIcons = [
  { icon: 'mdi-github', link: 'https://github.com/rajorshi' },
  { icon: 'mdi-linkedin', link: 'https://linkedin.com/in/rajorshi-tah' },
  { icon: 'mdi-twitter', link: 'https://twitter.com/rajorshitah' },
];

// Toggle dark/light theme
const toggleTheme = () => {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark';
  localStorage.setItem('theme', theme.global.name.value);
};

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

// Lifecycle hooks
onMounted(() => {
  window.addEventListener('resize', handleResize);
  
  // Load saved theme preference
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    theme.global.name.value = savedTheme;
  }
  
  // Close drawer on mobile when route changes
  if (isMobile.value) {
    drawer.value = false;
  }
});
</script>

<template>
  <v-app :theme="theme.global.name.value">
    <!-- App Bar -->
    <v-app-bar app :elevation="2">
      <v-app-bar-nav-icon 
        @click="drawer = !drawer" 
        class="d-flex d-lg-none"
      />
      
      <v-toolbar-title class="font-weight-bold">
        <router-link to="/" class="text-decoration-none text-uppercase">
          Rajorshi Tah
        </router-link>
      </v-toolbar-title>
      
      <v-spacer />
      
      <!-- Desktop Navigation -->
      <v-toolbar-items class="d-none d-lg-flex">
        <v-btn
          v-for="item in navItems"
          :key="item.title"
          :to="item.to"
          :prepend-icon="item.icon"
          variant="text"
          :active="isActive(item.to)"
          class="text-none"
        >
          {{ item.title }}
        </v-btn>
      </v-toolbar-items>
      
      <!-- Admin Profile Management Button -->
      <v-btn
        v-if="authStore.isAuthenticated"
        to="/profile-management"
        icon
        class="ml-2"
        title="Profile Management"
      >
        <v-icon>mdi-account-cog</v-icon>
      </v-btn>

      <!-- Login/Logout Button -->
      <v-btn
        v-if="!authStore.isAuthenticated"
        to="/login"
        icon
        class="ml-2"
        title="Login"
      >
        <v-icon>mdi-login</v-icon>
      </v-btn>

      <v-btn
        v-else
        @click="authStore.logout"
        icon
        class="ml-2"
        title="Logout"
      >
        <v-icon>mdi-logout</v-icon>
      </v-btn>

      <!-- Theme Toggle -->
      <v-btn 
        icon 
        @click="toggleTheme"
        class="ml-2"
        :title="theme.global.current.value.dark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
      >
        <v-icon>mdi-theme-light-dark</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Mobile Navigation Drawer -->
    <v-navigation-drawer 
      v-model="drawer" 
      app 
      temporary
      location="left"
      width="280"
    >
      <v-list nav>
        <v-list-item
          v-for="item in navItems"
          :key="item.title"
          :to="item.to"
          :prepend-icon="item.icon"
          :title="item.title"
          :active="isActive(item.to)"
          @click="drawer = false"
        />
      </v-list>
      
      <template v-slot:append>
        <div class="pa-4 text-center">
          <v-divider class="mb-4" />
          <div class="d-flex justify-center">
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
          </div>
          <div class="text-caption mt-2">
            {{ new Date().getFullYear() }} Rajorshi Tah
          </div>
        </div>
      </template>
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
