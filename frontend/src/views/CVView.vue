<script setup>
import { ref, onMounted, computed } from 'vue';
import { useDisplay } from 'vuetify';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import { 
  mdiFileAccount, 
  mdiFileDocument,
  mdiFileDocumentOutline,
  mdiFileDownload, 
  mdiDownload, 
  mdiCloudUpload, 
  mdiClose, 
  mdiCheck,
  mdiLock,
  mdiUpload,
  mdiLogin 
} from '@mdi/js';

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

// Handle file selection
const onFileSelected = (files) => {
  // This method is triggered when a file is selected
  // You can add additional validation or processing here if needed
  console.log('File selected:', files);
};
</script>

<template>
  <VContainer class="cv-container py-12">
    

    <!-- CV Card -->
    <VRow justify="center" class="mb-12">
      <VCol cols="12" md="10" lg="8" xl="6">
        <VCard class="pa-6" elevation="4" rounded="lg" style="overflow: visible;">
          <!-- Download Section -->
          <VCardTitle class="text-h5 mb-6 d-flex align-center">
            <VAvatar color="primary" variant="tonal" size="48" class="mr-4">
              <VIcon :icon="mdiFileAccount" size="24" />
            </VAvatar>
            <div>
              <div class="text-h5 font-weight-bold">Download CV</div>
              <div class="text-caption text-medium-emphasis">Get the latest version of my resume</div>
            </div>
          </VCardTitle>
          
          <VCardText class="text-center px-6 py-8">
            <VAvatar size="100" color="primary" variant="tonal" class="mb-6">
              <VIcon :icon="mdiFileDownload" size="48" color="primary" />
            </VAvatar>
            <p class="text-body-1 mb-6">
              Access my professional resume with detailed work experience, skills, and education history in a clean, printable format.
            </p>
            <VBtn
              color="primary"
              size="large"
              :loading="downloading"
              :disabled="!hasCV || downloading"
              @click="downloadCV"
              class="mt-2 px-8"
              rounded="pill"
              min-width="200"
              height="48"
            >
              <template v-slot:prepend>
                <VIcon :icon="mdiDownload" size="20" />
              </template>
              <span class="text-capitalize">Download CV</span>
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
              <VIcon :icon="mdiUpload" class="mr-3" color="primary" />
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
              
              <VCard
                variant="outlined"
                class="mb-4 text-center pa-4"
                :class="{ 'border-primary': file }"
                @click="!uploading && $refs.fileInput?.click()"
                :disabled="uploading"
                :ripple="!uploading"
                :elevation="file ? 2 : 0"
                style="cursor: pointer; transition: all 0.3s ease;"
              >
                <VFileInput
                  ref="fileInput"
                  v-model="file"
                  :rules="fileRules"
                  accept=".pdf,.doc,.docx"
                  label="Choose a file or drop it here"
                  :prepend-icon="mdiFileDocument"
                  variant="plain"
                  :loading="uploading"
                  :disabled="uploading"
                  class="d-none"
                  @update:model-value="onFileSelected"
                />
                <VAvatar
                  size="64"
                  :color="file ? 'primary' : 'grey-lighten-3'"
                  class="mb-2"
                >
                  <VIcon
                    :icon="file ? mdiFileDocument : mdiFileDocumentOutline"
                    size="32"
                    :color="file ? 'white' : 'grey-darken-1'"
                  />
                </VAvatar>
                <div class="text-body-1 font-weight-medium mb-1">
                  {{ file ? file[0]?.name || 'File selected' : 'Upload your CV' }}
                </div>
                <div class="text-caption text-medium-emphasis">
                  {{ file ? 'Click to change file' : 'PDF, DOC, DOCX (Max 5MB)' }}
                </div>
              </VCard>
              
              <VBtn
                color="primary"
                :loading="uploading"
                :disabled="!file || !file.length || uploading"
                block
                @click="uploadCV"
                rounded
              >
                <VIcon :icon="mdiCloudUpload" start />
                Upload CV
              </VBtn>
            </VCardText>
          </template>
          
          <VCardText v-else class="text-center pa-8 pb-10">
            <VAvatar size="100" color="grey-lighten-4" class="mb-6">
              <VIcon :icon="mdiLock" size="48" color="grey-darken-1" />
            </VAvatar>
            <h3 class="text-h6 font-weight-medium mb-2">Authentication Required</h3>
            <p class="text-body-2 text-medium-emphasis mb-6">
              Please sign in with admin privileges to upload a new CV document.
            </p>
            <VBtn
              color="primary"
              variant="outlined"
              :to="{ name: 'login', query: { redirect: '/cv' } }"
              class="mt-2 px-6"
              rounded="pill"
            >
              <template v-slot:prepend>
                <VIcon :icon="mdiLogin" size="20" />
              </template>
              Sign In
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
  position: relative;
  overflow: hidden;
}

.gradient-text {
  background: linear-gradient(45deg, var(--v-primary-base), #4caf50);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.v-card {
  border-radius: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  overflow: hidden;
}

.v-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px -4px rgba(0, 0, 0, 0.1) !important;
}

.v-btn {
  text-transform: none;
  letter-spacing: 0.5px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.v-btn--size-large {
  padding: 0 28px;
  height: 48px;
  font-size: 0.9375rem;
}

.v-avatar {
  transition: transform 0.3s ease;
}

.v-avatar:hover {
  transform: scale(1.05);
}

.max-w-2xl {
  max-width: 42rem;
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
