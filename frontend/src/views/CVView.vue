<script setup>
import { ref, onMounted, computed } from 'vue';
import { useDisplay } from 'vuetify';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const { mobile } = useDisplay();
const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);

// CV state
const hasCV = ref(false);
const lastUpdated = ref(null);
const downloading = ref(false);
const file = ref(null);
const uploading = ref(false);
const uploadSuccess = ref(false);
const uploadError = ref('');

// File validation rules
const fileRules = [
  value => {
    if (!value || !value.length) return true;
    const selectedFile = Array.isArray(value) ? value[0] : value;
    const fileExtension = selectedFile.name.split('.').pop().toLowerCase();
    const allowedExtensions = ['pdf', 'doc', 'docx'];
    return allowedExtensions.includes(fileExtension) || 'File must be a PDF or Word document';
  },
  value => {
    if (!value || !value.length) return true;
    const selectedFile = Array.isArray(value) ? value[0] : value;
    return selectedFile.size < 5 * 1024 * 1024 || 'File size should be less than 5MB';
  }
];

// Format date for display
const formatDate = (dateString) => {
  if (!dateString) return '';
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

// Check if CV exists
const checkCV = async () => {
  try {
    const response = await axios.head('/api/cv/download');
    hasCV.value = response.status === 200;
    if (response.headers['last-modified']) {
      lastUpdated.value = new Date(response.headers['last-modified']).toISOString();
    }
  } catch (error) {
    if (error.response && error.response.status === 404) {
      hasCV.value = false;
    } else {
      console.error('Error checking CV:', error);
    }
  }
};

// Download CV
const downloadCV = async () => {
  if (!hasCV.value) return;
  
  downloading.value = true;
  try {
    const response = await axios.get('/api/cv/download', {
      responseType: 'blob'
    });
    
    // Create a temporary URL for the blob
    const url = window.URL.createObjectURL(new Blob([response.data]));
    
    // Create a temporary link to trigger the download
    const link = document.createElement('a');
    link.href = url;
    
    // Extract filename from content-disposition header
    const contentDisposition = response.headers['content-disposition'];
    let filename = 'Rajorshi_Tah_CV.pdf';
    
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
      if (filenameMatch && filenameMatch[1]) {
        filename = filenameMatch[1].replace(/['"]/g, '');
      }
    }
    
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    
    // Clean up
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error downloading CV:', error);
    alert('Failed to download CV. Please try again.');
  } finally {
    downloading.value = false;
  }
};

// Upload CV
const uploadCV = async () => {
  if (!file.value || !file.value.length) {
    uploadError.value = 'Please select a file to upload.';
    return;
  }
  
  uploading.value = true;
  uploadSuccess.value = false;
  uploadError.value = '';
  
  const formData = new FormData();
  // Handle array of files from v-file-input
  const selectedFile = Array.isArray(file.value) ? file.value[0] : file.value;
  formData.append('file', selectedFile);
  
  try {
    const response = await axios.post('/api/cv/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${authStore.token}`
      }
    });
    
    // Reset form and show success message
    file.value = null;
    uploadSuccess.value = true;
    
    // Update CV status
    await checkCV();
    
    // Hide success message after 5 seconds
    setTimeout(() => {
      uploadSuccess.value = false;
    }, 5000);
  } catch (error) {
    console.error('Error uploading CV:', error);
    uploadError.value = error.response?.data?.message || 'Failed to upload CV. Please try again.';
  } finally {
    uploading.value = false;
  }
};

// Check CV status on component mount
onMounted(() => {
  checkCV();
});
</script>

<template>
  <VContainer class="cv-container py-8">
    <!-- Header -->
    <VRow>
      <VCol cols="12" class="text-center">
        <h1 class="text-h3 font-weight-bold mb-2">My CV</h1>
        <p class="text-body-1 text-medium-emphasis mb-8">
          Download my latest resume or upload a new version (admin only)
        </p>
      </VCol>
    </VRow>

    <!-- CV Card -->
    <VRow justify="center">
      <VCol cols="12" md="8" lg="6">
        <VCard class="pa-6" elevation="2">
          <!-- Download Section -->
          <VCardTitle class="text-h5 mb-4 d-flex align-center">
            <VIcon icon="mdi-file-account" class="mr-3" color="primary" />
            Download CV
          </VCardTitle>
          
          <VCardText class="text-center">
            <VIcon size="64" color="primary" class="mb-4">mdi-file-download</VIcon>
            <p class="text-body-1 mb-4">
              Click the button below to download my latest CV in PDF format.
            </p>
            <VBtn
              color="primary"
              size="large"
              :loading="downloading"
              :disabled="!hasCV"
              @click="downloadCV"
              class="mb-4"
              rounded
            >
              <VIcon start>mdi-download</VIcon>
              Download CV
            </VBtn>
            
            <VAlert
              v-if="!hasCV"
              type="info"
              variant="tonal"
              class="mb-4"
            >
              No CV has been uploaded yet.
            </VAlert>
            
            <p v-if="lastUpdated" class="text-caption text-medium-emphasis mt-2">
              Last updated: {{ formatDate(lastUpdated) }}
            </p>
          </VCardText>
          
          <VDivider class="my-6" />
          
          <!-- Admin Section -->
          <template v-if="isAuthenticated">
            <VCardTitle class="text-h5 mb-4 d-flex align-center">
              <VIcon icon="mdi-upload" class="mr-3" color="primary" />
              Upload New CV
            </VCardTitle>
            
            <VCardText>
              <VAlert
                v-if="uploadSuccess"
                type="success"
                variant="tonal"
                class="mb-4"
              >
                CV uploaded successfully!
              </VAlert>
              
              <VAlert
                v-if="uploadError"
                type="error"
                variant="tonal"
                class="mb-4"
              >
                {{ uploadError }}
              </VAlert>
              
              <VFileInput
                v-model="file"
                :rules="fileRules"
                accept=".pdf,.doc,.docx"
                label="CV File"
                prepend-icon="mdi-file"
                variant="outlined"
                :loading="uploading"
                :disabled="uploading"
                class="mb-4"
              />
              
              <VBtn
                color="primary"
                :loading="uploading"
                :disabled="!file || !file.length || uploading"
                block
                @click="uploadCV"
                rounded
              >
                <VIcon start>mdi-upload</VIcon>
                Upload CV
              </VBtn>
            </VCardText>
          </template>
          
          <VCardText v-else class="text-center">
            <VIcon size="48" color="primary" class="mb-4">mdi-lock</VIcon>
            <p class="text-body-1 mb-4">
              Admin access is required to upload a new CV.
            </p>
            <VBtn
              color="primary"
              variant="text"
              :to="{ name: 'login', query: { redirect: '/cv' } }"
              class="mt-2"
            >
              Login
            </VBtn>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>
  </VContainer>
</template>

<style scoped>
.cv-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px;
}

.v-card {
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.v-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
}

.v-btn {
  text-transform: none;
  letter-spacing: normal;
}

/* Responsive adjustments */
@media (max-width: 960px) {
  .cv-container {
    padding: 16px 12px;
  }
  
  h1 {
    font-size: 2rem !important;
  }
}
</style>
