<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useDisplay } from 'vuetify';
import { useAuthStore } from '@/stores/auth';
import { 
  mdiPencil, 
  mdiPlus, 
  mdiMagnify, 
  mdiFolderTextOutline, 
  mdiDelete, 
  mdiFolderOpenOutline, 
  mdiClose, 
  mdiDomain, 
  mdiCalendarRange, 
  mdiCalendarMonth, 
  mdiCheckCircle, 
  mdiOpenInNew 
} from '@mdi/js';
import axios from 'axios';

const authStore = useAuthStore();

const { mobile } = useDisplay();
const route = useRoute();

// State
const projects = ref([]);
const isLoading = ref(true);
const searchQuery = ref('');
const activeFilter = ref('all');


// Computed properties
const filteredProjects = computed(() => {
  const query = searchQuery.value?.toLowerCase().trim();
  
  return projects.value.filter(project => {
    // Filter by search query
    const matchesSearch = !query || 
      // Search in title
      (project.title && project.title.toLowerCase().includes(query)) ||
      // Search in description
      (project.description && project.description.toLowerCase().includes(query)) ||
      // Search in company
      (project.company && project.company.toLowerCase().includes(query)) ||
      // Search in highlights
      (project.highlights && project.highlights.some(highlight => 
        highlight && highlight.toLowerCase().includes(query)
      ));
    
    // Filter by project type
    const matchesType = activeFilter.value === 'all' || 
      project.type === activeFilter.value ||
      (activeFilter.value === 'ai' && project.tech_stack && 
       project.tech_stack.some(tech => tech.toLowerCase().includes('ai') || tech.toLowerCase().includes('ml')));
    
    // Debug log
    if (query) {
      console.log('Searching for:', query);
      console.log('Project:', project.title);
      console.log('Tech Stack:', project.tech_stack);
      console.log('Matches search:', matchesSearch);
      console.log('Matches type:', matchesType);
    }
    
    return matchesSearch && matchesType;
  });
});

// Fetch projects from API
const fetchProjects = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get('/api/projects');
    projects.value = response.data;
  } catch (error) {
    console.error('Error fetching projects:', error);
  } finally {
    isLoading.value = false;
  }
};

// Format date
const formatDate = (dateString) => {
  if (!dateString) return '';
  const options = { year: 'numeric', month: 'long' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

// Get project image with fallback
const getProjectImage = (project) => {
  return project.image || project.thumbnail || '/project-placeholder.jpg';
};

// Open project details
const openProjectDialog = (project) => {
  selectedProject.value = project;
  dialog.value = true;
};

// Lifecycle hooks
onMounted(() => {
  fetchProjects();
  
  // Check for type filter in URL
  if (route.query.type) {
    activeFilter.value = route.query.type;
  }
});

// Dialog state
const dialog = ref(false);
const selectedProject = ref(null);
const showAddProjectDialog = ref(false);
const showEditProjectDialog = ref(false);
const isSaving = ref(false);
const form = ref(null);
const editForm = ref(null);

// Project form data
const newProject = ref({
  title: '',
  company: '',
  description: '',
  technologies: [],
  highlights: [''],
  start_date: new Date().toISOString().substr(0, 10),
  end_date: ''
});

// Add new project
const addNewProject = () => {
  // Reset form
  newProject.value = {
    title: '',
    company: '',
    description: '',
    technologies: [],
    highlights: [''],
    start_date: new Date().toISOString().substr(0, 10),
    end_date: ''
  };
  showAddProjectDialog.value = true;
};

// Add a new highlight field
const addHighlight = () => {
  newProject.value.highlights.push('');
};

// Remove a highlight field
const removeHighlight = (index) => {
  if (newProject.value.highlights.length > 1) {
    newProject.value.highlights.splice(index, 1);
  }
};

// Save new project
const saveProject = async () => {
  const { valid } = await form.value.validate();
  if (!valid) return;

  isSaving.value = true;
  
  try {
    const payload = {
      ...newProject.value,
      highlights: newProject.value.highlights.filter(h => h.trim() !== '')
    };
    
    const response = await axios.post('/api/projects', payload, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    });
    
    // Show success message
    showSnackbar('Project created successfully', 'success');
    
    // Add the new project to the beginning of the list
    if (response.data.id) {
      const newProjectWithId = { ...payload, _id: response.data.id };
      projects.value.unshift(newProjectWithId);
    } else {
      // If ID is not in response, refresh the list
      await fetchProjects();
    }
    
    showAddProjectDialog.value = false;
  } catch (error) {
    console.error('Error saving project:', error);
    const errorMessage = error.response?.data?.error || 'Failed to create project';
    showSnackbar(errorMessage, 'error');
  } finally {
    isSaving.value = false;
  }
};

// Edit project
const editProject = (project) => {
  selectedProject.value = { ...project };
  showEditProjectDialog.value = true;
};

// Update project
const updateProject = async () => {
  const { valid } = await editForm.value.validate();
  if (!valid || !selectedProject.value?._id) return;

  isSaving.value = true;
  
  try {
    const payload = {
      ...selectedProject.value,
      highlights: Array.isArray(selectedProject.value.highlights) 
        ? selectedProject.value.highlights.filter(h => h.trim() !== '')
        : [],
      technologies: Array.isArray(selectedProject.value.technologies)
        ? selectedProject.value.technologies
        : []
    };
    
    const response = await axios.put(`/api/projects/${selectedProject.value._id}`, payload, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    });
    
    // Show success message
    showSnackbar('Project updated successfully', 'success');
    
    // Update the project in the local state
    const updatedProject = response.data.project;
    const index = projects.value.findIndex(p => p._id === updatedProject._id);
    if (index !== -1) {
      projects.value[index] = updatedProject;
    }
    
    showEditProjectDialog.value = false;
  } catch (error) {
    console.error('Error updating project:', error);
    const errorMessage = error.response?.data?.error || 'Failed to update project';
    showSnackbar(errorMessage, 'error');
  } finally {
    isSaving.value = false;
  }
};

// Delete project
const deleteProject = async (projectId, event) => {
  event.stopPropagation();
  
  if (!confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
    return;
  }
  
  try {
    await axios.delete(`/api/projects/${projectId}`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    });
    
    // Remove the project from the local state
    projects.value = projects.value.filter(project => project._id !== projectId);
    
    showSnackbar('Project deleted successfully', 'success');
  } catch (error) {
    console.error('Error deleting project:', error);
    const errorMessage = error.response?.data?.error || 'Failed to delete project';
    showSnackbar(errorMessage, 'error');
  }
};

// Show snackbar notification
const snackbar = ref({
  show: false,
  message: '',
  color: 'success'
});

const showSnackbar = (message, color = 'success') => {
  snackbar.value = {
    show: true,
    message,
    color
  };
};
</script>

<template>
  <VContainer class="portfolio-container py-8">
    <!-- Header -->
    <VRow class="mb-8 align-center">
      <VCol cols="12" md="8">
        <h1 class="text-h3 text-center text-md-start mb-2">My Portfolio</h1>
        <p class="text-body-1 text-medium-emphasis text-center text-md-start mb-0">
          A collection of my professional projects and work
        </p>
      </VCol>
      <VCol cols="12" md="4" class="text-center text-md-end mt-4 mt-md-0">
        <VBtn
          v-if="authStore.isAuthenticated"
          color="primary"
          :prepend-icon="mdiPlus"
          @click="addNewProject"
          class="text-none"
          elevation="1"
        >
          Add Project
        </VBtn>
      </VCol>
    </VRow>

    <!-- Search and Filters -->
    <VRow class="mb-6">
      <VCol cols="12">
        <VTextField
          v-model="searchQuery"
          label="Search projects..."
          :prepend-inner-icon="mdiMagnify"
          variant="outlined"
          density="comfortable"
          hide-details
          clearable
          @click:clear="searchQuery = ''"
        />
      </VCol>
    </VRow>


    <!-- Projects Grid -->
    <VRow v-if="isLoading">
      <VCol
        v-for="n in 6"
        :key="n"
        cols="12"
        sm="6"
        lg="4"
      >
        <VSkeletonLoader type="card" />
      </VCol>
    </VRow>

    <VRow v-else-if="filteredProjects.length > 0" class="project-grid">
      <VCol
        v-for="project in filteredProjects"
        :key="project._id"
        cols="12"
      >
        <VCard
          class="project-card"
          elevation="2"
          hover
          @click="openProjectDialog(project)"
        >
          <VCardItem class="px-6 pt-6 pb-0">
            <template v-slot:prepend>
              <VAvatar
                color="primary"
                variant="tonal"
                size="56"
                class="mr-4"
              >
                <VIcon size="32" :icon="mdiFolderTextOutline" />
              </VAvatar>
            </template>
            
            <VCardTitle class="text-h5">{{ project.title }}</VCardTitle>
            <VCardSubtitle class="text-medium-emphasis">
              {{ project.company || 'Personal Project' }} • {{ formatDate(project.date) }}
            </VCardSubtitle>
          </VCardItem>
          
          <VCardText class="px-6 py-0" style="flex-grow: 1;">
            <p class="text-body-1 mb-4">
              {{ project.summary || (project.description ? project.description.substring(0, 200) + (project.description.length > 200 ? '...' : '') : 'No description available.') }}
            </p>
            
            <div v-if="project.tech_stack && project.tech_stack.length > 0" class="mb-4">
              <VChip
                v-for="(tech, index) in project.tech_stack.slice(0, 5)"
                :key="index"
                size="small"
                color="primary"
                variant="outlined"
                class="mr-2 mb-2"
                label
              >
                {{ tech }}
              </VChip>
            </div>
            
            <div v-if="project.highlights && project.highlights.length > 0" class="mt-2">
              <div v-for="(highlight, index) in project.highlights" :key="index" class="d-flex align-start mb-2">
                <VIcon :icon="mdiCheckCircle" size="small" class="mr-2 mt-1" color="primary" />
                <span class="text-body-2">{{ highlight }}</span>
              </div>
            </div>
          </VCardText>
          
          <VCardActions class="px-6 pb-1 pt-0" style="margin-top: auto;">
            <VSpacer />
            <VBtn
              v-if="authStore.isAuthenticated"
              color="primary"
              variant="text"
              size="small"
              @click.stop="editProject(project)"
              class="text-none mr-2"
            >
              <VIcon :icon="mdiPencil" />
              <span class="ml-1">Edit</span>
            </VBtn>
            <VBtn
              v-if="authStore.isAuthenticated"
              color="error"
              variant="text"
              size="small"
              @click.stop="deleteProject(project._id, $event)"
              class="text-none"
            >
              <VIcon :icon="mdiDelete" />
              <span class="ml-1">Delete</span>
            </VBtn>
          </VCardActions>
        </VCard>
      </VCol>
    </VRow>

    <VRow v-else>
      <VCol cols="12" class="text-center py-12">
        <VIcon :icon="mdiFolderOpenOutline" size="64" class="mb-4" color="grey-lighten-1" />
        <h3 class="text-h6 mb-2">No projects found</h3>
        <p class="text-body-2 text-medium-emphasis mb-4">
          {{ activeFilter === 'all' ? 'No projects available yet.' : `No ${activeFilter} projects found.` }}
        </p>
        <VBtn
          v-if="activeFilter !== 'all' || searchQuery"
          color="primary"
          variant="text"
          @click="{
            activeFilter = 'all';
            searchQuery = '';
          }"
        >
          Clear filters
        </VBtn>
      </VCol>
    </VRow>
    
    <!-- Project Details Dialog -->
    <VDialog v-model="dialog" max-width="800" scrollable>
      <VCard v-if="selectedProject">
        <VToolbar color="primary">
          <VToolbarTitle class="text-white">{{ selectedProject.title }}</VToolbarTitle>
          <VSpacer />
          <VBtn icon @click="dialog = false">
            <VIcon :icon="mdiClose" />
          </VBtn>
        </VToolbar>
        
        <VCardText class="pt-6">
          <div class="d-flex flex-wrap align-center gap-4 mb-4">
            <VChip v-if="selectedProject.company" color="primary" variant="flat" size="small">
              <template #prepend><VIcon :icon="mdiDomain" /></template>
              {{ selectedProject.company }}
            </VChip>
            
            <VChip variant="outlined" size="small" v-if="selectedProject.duration">
              <template #prepend><VIcon :icon="mdiCalendarRange" /></template>
              {{ selectedProject.duration }}
            </VChip>
            
            <VChip 
              v-else-if="selectedProject.date"
              variant="outlined" 
              size="small"
            >
              <template #prepend><VIcon :icon="mdiCalendarMonth" /></template>
              {{ formatDate(selectedProject.date) }}
            </VChip>
            
          </div>
          
          <div class="mb-6">
            <h3 class="text-h6 mb-2">Project Description</h3>
            <p class="text-body-1">{{ selectedProject.description || 'No description available.' }}</p>
          </div>
          
          <div v-if="selectedProject.highlights && selectedProject.highlights.length > 0" class="mb-6">
            <h3 class="text-h6 mb-3">Key Features</h3>
            <VList density="compact" class="bg-transparent">
              <VListItem
                v-for="(highlight, index) in selectedProject.highlights"
                :key="index"
                class="px-0"
              >
                <template v-slot:prepend>
                  <VIcon :icon="mdiCheckCircle" color="primary" size="small" class="mr-2" />
                </template>
                <VListItemTitle class="text-body-2">{{ highlight }}</VListItemTitle>
              </VListItem>
            </VList>
          </div>
          
          <div v-if="selectedProject.links && Object.keys(selectedProject.links).length > 0" class="mb-6">
            <h3 class="text-h6 mb-3">Links</h3>
            <div class="d-flex flex-wrap gap-2">
              <VBtn
                v-for="(url, label) in selectedProject.links"
                :key="label"
                :href="url"
                target="_blank"
                rel="noopener noreferrer"
                color="primary"
                variant="outlined"
                size="small"
                class="text-none"
              >
                <VIcon start>{{ getLinkIcon(label) }}</VIcon>
                {{ label }}
              </VBtn>
            </div>
          </div>
          
          <div v-if="selectedProject.testimonial" class="bg-grey-lighten-4 pa-4 rounded">
            <p class="text-body-2 font-italic mb-2">"{{ selectedProject.testimonial.text }}"</p>
            <div class="d-flex align-center">
              <VAvatar size="36" class="mr-2">
                <VImg :src="selectedProject.testimonial.avatar || '/avatar-placeholder.png'" />
              </VAvatar>
              <div>
                <div class="font-weight-medium">{{ selectedProject.testimonial.name }}</div>
                <div class="text-caption text-medium-emphasis">{{ selectedProject.testimonial.role }}</div>
              </div>
            </div>
          </div>
        </VCardText>
        
        <VCardActions class="px-4 pb-4">
          <VSpacer />
          <VBtn
            color="primary"
            variant="text"
            @click="dialog = false"
          >
            Close
          </VBtn>
          <VBtn
            v-if="selectedProject.demo"
            color="primary"
            :href="selectedProject.demo"
            target="_blank"
            rel="noopener noreferrer"
          >
            <template #prepend><VIcon :icon="mdiOpenInNew" /></template>
            View Live
          </VBtn>
        </VCardActions>
      </VCard>
    </VDialog>
    <!-- Add Project Dialog -->
    <VDialog v-model="showAddProjectDialog" max-width="800">
      <VForm ref="form" @submit.prevent="saveProject">
        <VCard>
          <VToolbar color="primary">
            <VToolbarTitle class="text-white">Add New Project</VToolbarTitle>
            <VSpacer />
            <VBtn icon @click="showAddProjectDialog = false">
              <VIcon :icon="mdiClose" />
            </VBtn>
          </VToolbar>
          
          <VCardText class="pt-6">
            <VRow>
              <VCol cols="12" md="6">
                <VTextField
                  v-model="newProject.title"
                  label="Project Title"
                  :rules="[v => !!v || 'Title is required']"
                  required
                />
              </VCol>
              <VCol cols="12" md="6">
                <VTextField
                  v-model="newProject.company"
                  label="Company"
                  :rules="[v => !!v || 'Company is required']"
                  required
                />
              </VCol>
              <VCol cols="12">
                <VTextarea
                  v-model="newProject.description"
                  label="Description"
                  rows="3"
                  :rules="[v => !!v || 'Description is required']"
                  required
                />
              </VCol>
              <VCol cols="12">
                <div class="d-flex align-center mb-2">
                  <VLabel>Highlights</VLabel>
                  <VBtn
                    size="x-small"
                    variant="text"
                    color="primary"
                    class="ml-2"
                    @click="addHighlight"
                  >
                    <VIcon :icon="mdiPlus" size="small" />
                    <span class="ml-1">Add Highlight</span>
                  </VBtn>
                </div>
                <VTextField
                  v-for="(highlight, index) in newProject.highlights"
                  :key="index"
                  v-model="newProject.highlights[index]"
                  :label="`Highlight ${index + 1}`"
                  class="mb-2"
                  :rules="[v => !!v || 'Highlight cannot be empty']"
                  required
                >
                  <template v-slot:append>
                    <VBtn
                      :icon="mdiClose"
                      variant="text"
                      @click.stop="removeHighlight(index)"
                    />
                  </template>
                </VTextField>
              </VCol>
              <VCol cols="12">
                <VCombobox
                  v-model="newProject.technologies"
                  label="Technologies"
                  multiple
                  chips
                  :items="[]"
                  hint="Type and press enter to add a technology"
                  persistent-hint
                />
              </VCol>
              <VCol cols="12" md="6">
                <VTextField
                  v-model="newProject.start_date"
                  label="Start Date"
                  type="date"
                  :max="newProject.end_date || null"
                />
              </VCol>
              <VCol cols="12" md="6">
                <VTextField
                  v-model="newProject.end_date"
                  label="End Date (leave empty if ongoing)"
                  type="date"
                  :min="newProject.start_date || null"
                />
              </VCol>
            </VRow>
          </VCardText>
          
          <VCardActions class="px-6 pb-4">
            <VSpacer />
            <VBtn
              color="primary"
              variant="text"
              @click="showAddProjectDialog = false"
              :disabled="isSaving"
            >
              Cancel
            </VBtn>
            <VBtn
              color="primary"
              type="submit"
              :loading="isSaving"
            >
              Save Project
            </VBtn>
          </VCardActions>
        </VCard>
      </VForm>
    </VDialog>

    <!-- Edit Project Dialog -->
    <VDialog v-model="showEditProjectDialog" max-width="800">
      <VForm v-if="selectedProject" ref="editForm" @submit.prevent="updateProject">
        <VCard>
          <VToolbar color="primary">
            <VToolbarTitle class="text-white">Edit Project</VToolbarTitle>
            <VSpacer />
            <VBtn icon @click="showEditProjectDialog = false">
              <VIcon :icon="mdiClose" />
            </VBtn>
          </VToolbar>
          
          <VCardText class="pt-6">
            <VRow>
              <VCol cols="12" md="6">
                <VTextField
                  v-model="selectedProject.title"
                  label="Project Title"
                  :rules="[v => !!v || 'Title is required']"
                  required
                />
              </VCol>
              <VCol cols="12" md="6">
                <VTextField
                  v-model="selectedProject.company"
                  label="Company"
                  :rules="[v => !!v || 'Company is required']"
                  required
                />
              </VCol>
              <VCol cols="12">
                <VTextarea
                  v-model="selectedProject.description"
                  label="Description"
                  rows="3"
                  :rules="[v => !!v || 'Description is required']"
                  required
                />
              </VCol>
              <VCol cols="12">
                <div class="d-flex align-center mb-2">
                  <VLabel>Highlights</VLabel>
                  <VBtn
                    size="x-small"
                    variant="text"
                    color="primary"
                    class="ml-2"
                    @click="selectedProject.highlights ? selectedProject.highlights.push('') : (selectedProject.highlights = [''])"
                  >
                    <VIcon :icon="mdiPlus" size="small" />
                    <span class="ml-1">Add Highlight</span>
                  </VBtn>
                </div>
                <VTextField
                  v-for="(highlight, index) in (selectedProject.highlights || [])"
                  :key="index"
                  v-model="selectedProject.highlights[index]"
                  :label="`Highlight ${index + 1}`"
                  class="mb-2"
                  :rules="[v => !!v || 'Highlight cannot be empty']"
                  required
                >
                  <template v-slot:append>
                    <VBtn
                      :icon="mdiClose"
                      variant="text"
                      @click.stop="selectedProject.highlights.splice(index, 1)"
                      :disabled="!selectedProject.highlights || selectedProject.highlights.length <= 1"
                    />
                  </template>
                </VTextField>
              </VCol>
              <VCol cols="12">
                <VCombobox
                  v-model="selectedProject.technologies"
                  label="Technologies"
                  multiple
                  chips
                  :items="[]"
                  hint="Type and press enter to add a technology"
                  persistent-hint
                />
              </VCol>
              <VCol cols="12" md="6">
                <VTextField
                  v-model="selectedProject.start_date"
                  label="Start Date"
                  type="date"
                  :max="selectedProject.end_date || null"
                />
              </VCol>
              <VCol cols="12" md="6">
                <VTextField
                  v-model="selectedProject.end_date"
                  label="End Date (leave empty if ongoing)"
                  type="date"
                  :min="selectedProject.start_date || null"
                />
              </VCol>
            </VRow>
          </VCardText>
          
          <VCardActions class="px-6 pb-4">
            <VSpacer />
            <VBtn
              color="primary"
              variant="text"
              @click="showEditProjectDialog = false"
              :disabled="isSaving"
            >
              Cancel
            </VBtn>
            <VBtn
              color="primary"
              type="submit"
              :loading="isSaving"
            >
              Update Project
            </VBtn>
          </VCardActions>
        </VCard>
      </VForm>
    </VDialog>

    <!-- Notification Snackbar -->
    <VSnackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
      location="top right"
    >
      {{ snackbar.message }}
      <template v-slot:actions>
        <VBtn
          icon
          @click="snackbar.show = false"
        >
          <VIcon :icon="mdiClose" />
        </VBtn>
      </template>
    </VSnackbar>
  </VContainer>
</template>

<style scoped>
.portfolio-container {
  max-width: 1200px;
}

.project-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1) !important;
}

.project-grid {
  margin-top: 16px;
  margin: 0 auto;
  padding: 24px 16px;
}

/* Smooth scrolling for anchor links */
html {
  scroll-behavior: smooth;
}

/* Project card hover effect */
.v-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
}

.v-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
}

/* Responsive adjustments */
@media (max-width: 960px) {
  .portfolio-container {
    padding: 16px 12px;
  }
  
  h1 {
    font-size: 2rem !important;
  }
  
  h2 {
    font-size: 1.5rem !important;
  }
  
  h3 {
    font-size: 1.25rem !important;
  }
}

/* Custom scrollbar for dialog */
:deep(.v-dialog > .v-overlay__content > .v-card) {
  scrollbar-width: thin;
  scrollbar-color: rgba(var(--v-theme-primary), 0.5) transparent;
}

:deep(.v-dialog > .v-overlay__content > .v-card)::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

:deep(.v-dialog > .v-overlay__content > .v-card)::-webkit-scrollbar-track {
  background: transparent;
}

:deep(.v-dialog > .v-overlay__content > .v-card)::-webkit-scrollbar-thumb {
  background-color: rgba(var(--v-theme-primary), 0.5);
  border-radius: 20px;
}

/* Animation for project cards */
.v-col {
  transition: all 0.3s ease;
}

/* Fade in animation for content */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.v-col {
  animation: fadeIn 0.5s ease forwards;
}

/* Staggered animation for grid items */
.v-col:nth-child(2) { animation-delay: 0.1s; }
.v-col:nth-child(3) { animation-delay: 0.2s; }
.v-col:nth-child(4) { animation-delay: 0.3s; }
.v-col:nth-child(5) { animation-delay: 0.4s; }
.v-col:nth-child(6) { animation-delay: 0.5s; }
</style>
