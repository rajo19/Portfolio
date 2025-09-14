<template>
  <v-card class="profile-picture-upload">
    <v-card-title>
      <v-icon :icon="mdiAccountCircle" start />
      Profile Picture Management
    </v-card-title>
    
    <v-card-text>
      <!-- Current Profile Picture Display -->
      <div class="text-center mb-6">
        <v-avatar size="150" class="mb-4">
          <v-img
            :src="currentProfilePicture"
            :alt="profileData?.name || 'Profile Picture'"
            class="elevation-4"
          >
            <template v-slot:error>
              <v-icon :icon="mdiAccountCircle" size="80" color="grey-lighten-1" />
            </template>
          </v-img>
        </v-avatar>
        
        <div class="text-h6 mb-2">{{ profileData?.name || 'Profile Picture' }}</div>
      </div>

      <!-- Upload Section -->
      <v-divider class="mb-4"></v-divider>
      
      <div class="upload-section">
        <v-file-input
          v-model="selectedFile"
          label="Choose profile picture"
          accept="image/png,image/jpg,image/jpeg,image/gif,image/webp"
          :prepend-icon="mdiCamera"
          show-size
          :rules="fileRules"
          :loading="uploading"
          @change="onFileSelect"
          clearable
        >
          <template v-slot:selection="{ fileNames }">
            <template v-for="fileName in fileNames" :key="fileName">
              {{ fileName }}
            </template>
          </template>
        </v-file-input>

        <v-alert
          v-if="uploadError"
          type="error"
          class="mb-4"
          closable
          @click:close="uploadError = null"
        >
          {{ uploadError }}
        </v-alert>

        <v-alert
          v-if="uploadSuccess"
          type="success"
          class="mb-4"
          closable
          @click:close="uploadSuccess = null"
        >
          {{ uploadSuccess }}
        </v-alert>

        <!-- Preview Section -->
        <div v-if="previewUrl" class="preview-section mb-4">
          <v-card variant="outlined" class="pa-4">
            <div class="text-subtitle-1 mb-2">Preview:</div>
            <v-avatar size="100">
              <v-img :src="previewUrl" alt="Preview"></v-img>
            </v-avatar>
          </v-card>
        </div>

        <!-- Action Buttons -->
        <div class="d-flex gap-2">
          <v-btn
            color="primary"
            :disabled="!selectedFile || uploading"
            :loading="uploading"
            @click="uploadProfilePicture"
          >
            <v-icon :icon="mdiUpload" start />
            Upload Picture
          </v-btn>

          <v-btn
            v-if="currentFilename"
            color="error"
            variant="outlined"
            :disabled="uploading"
            @click="deleteProfilePicture"
          >
            <v-icon :icon="mdiDelete" start />
            Delete Current
          </v-btn>

          <v-btn
            variant="outlined"
            @click="resetForm"
            :disabled="uploading"
          >
            <v-icon :icon="mdiRefresh" start />
            Reset
          </v-btn>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import {
  mdiAccountCircle,
  mdiCamera,
  mdiUpload,
  mdiDelete,
  mdiRefresh
} from '@mdi/js'

const authStore = useAuthStore()

// Reactive data
const selectedFile = ref(null)
const uploading = ref(false)
const uploadError = ref(null)
const uploadSuccess = ref(null)
const previewUrl = ref(null)
const profileData = ref(null)
const currentFilename = ref(null)

// File validation rules
const fileRules = [
  value => {
    if (!value) return true
    
    // Handle both single file and array of files
    const file = Array.isArray(value) ? value[0] : value
    
    if (!file || !(file instanceof File)) {
      return 'Please select a valid file'
    }
    
    if (file.size > 5 * 1024 * 1024) {
      return 'File size must be less than 5MB'
    }
    
    const allowedTypes = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif', 'image/webp']
    if (!allowedTypes.includes(file.type)) {
      return 'File must be PNG, JPG, JPEG, GIF, or WEBP'
    }
    
    return true
  }
]

// Computed properties
const currentProfilePicture = computed(() => {
  if (profileData.value?.profile_picture && profileData.value.profile_picture !== '/api/profile/picture') {
    return `${axios.defaults.baseURL}${profileData.value.profile_picture}`
  }
  return 'https://via.placeholder.com/150?text=No+Image'
})

// Methods
const fetchProfileData = async () => {
  try {
    const response = await axios.get('/api/profile')
    profileData.value = response.data
    
    // Extract filename from profile picture URL if it exists
    if (response.data.profile_picture && response.data.profile_picture !== '/api/profile/picture') {
      const urlParts = response.data.profile_picture.split('/')
      currentFilename.value = urlParts[urlParts.length - 1]
    }
  } catch (error) {
    console.error('Failed to fetch profile data:', error)
  }
}

const onFileSelect = (files) => {
  uploadError.value = null
  uploadSuccess.value = null
  
  // Handle both single file and array of files
  const file = Array.isArray(files) ? files[0] : files
  
  if (file && file instanceof File) {
    // Create preview URL
    previewUrl.value = URL.createObjectURL(file)
    console.log('Selected file:', file.name, 'Size:', file.size, 'Type:', file.type)
  } else {
    previewUrl.value = null
  }
}

const uploadProfilePicture = async () => {
  if (!selectedFile.value) return
  
  // Get the actual file object
  const file = Array.isArray(selectedFile.value) ? selectedFile.value[0] : selectedFile.value
  
  if (!file || !(file instanceof File)) {
    uploadError.value = 'Please select a valid file'
    return
  }
  
  console.log('Uploading file:', file.name, 'Size:', file.size, 'Type:', file.type)
  
  // Validate file
  const validation = fileRules[0](file)
  if (validation !== true) {
    uploadError.value = validation
    return
  }

  uploading.value = true
  uploadError.value = null
  uploadSuccess.value = null

  try {
    const formData = new FormData()
    formData.append('file', file)

    console.log('FormData created with file:', file.name)

    const response = await axios.post('/api/profile/picture', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${authStore.token}`
      }
    })

    console.log('Upload response:', response.data)
    uploadSuccess.value = response.data.message
    currentFilename.value = response.data.filename
    
    // Refresh profile data to show new picture
    await fetchProfileData()
    
    // Reset form
    resetForm()
    
  } catch (error) {
    console.error('Upload failed:', error)
    uploadError.value = error.response?.data?.message || 'Upload failed. Please try again.'
  } finally {
    uploading.value = false
  }
}

const deleteProfilePicture = async () => {
  if (!currentFilename.value) return

  uploading.value = true
  uploadError.value = null
  uploadSuccess.value = null

  try {
    await axios.delete('/api/profile/picture', {
      data: { filename: currentFilename.value },
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })

    uploadSuccess.value = 'Profile picture deleted successfully'
    currentFilename.value = null
    
    // Refresh profile data
    await fetchProfileData()
    
  } catch (error) {
    console.error('Delete failed:', error)
    uploadError.value = error.response?.data?.message || 'Delete failed. Please try again.'
  } finally {
    uploading.value = false
  }
}

const resetForm = () => {
  selectedFile.value = null
  previewUrl.value = null
  uploadError.value = null
  uploadSuccess.value = null
}

// Lifecycle
onMounted(() => {
  fetchProfileData()
})
</script>

<style scoped>
.profile-picture-upload {
  max-width: 600px;
  margin: 0 auto;
}

.upload-section {
  max-width: 400px;
  margin: 0 auto;
}

.preview-section {
  text-align: center;
}

.gap-2 {
  gap: 8px;
}
</style>
