<template>
  <v-container class="profile-management-container">
    <v-row>
      <v-col cols="12">
        <v-card class="pa-6">
          <v-card-title class="text-h4 mb-6">
            <v-icon start>mdi-account-cog</v-icon>
            Profile Management
          </v-card-title>
          
          <!-- Authentication Check -->
          <div v-if="!authStore.isAuthenticated" class="text-center py-8">
            <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-lock</v-icon>
            <div class="text-h6 mb-4">Authentication Required</div>
            <div class="text-body-1 mb-4">You need to be logged in to manage your profile.</div>
            <v-btn color="primary" to="/login">
              <v-icon start>mdi-login</v-icon>
              Login
            </v-btn>
          </div>

          <!-- Profile Management Content -->
          <div v-else>
            <ProfilePictureUpload />
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import ProfilePictureUpload from '@/components/ProfilePictureUpload.vue'

const authStore = useAuthStore()
</script>

<style scoped>
.profile-management-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px;
}
</style>
