<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useDisplay } from 'vuetify';
import axios from 'axios';

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
</script>

<template>
  <VContainer class="portfolio-container py-8">
    <!-- Header -->
    <VRow class="mb-8">
      <VCol cols="12">
        <h1 class="text-h3 text-center text-md-start mb-2">My Portfolio</h1>
        <p class="text-body-1 text-medium-emphasis text-center text-md-start">
          A collection of my professional projects and work
        </p>
      </VCol>
    </VRow>

    <!-- Search and Filters -->
    <VRow class="mb-6">
      <VCol cols="12">
        <VTextField
          v-model="searchQuery"
          label="Search projects..."
          prepend-inner-icon="mdi-magnify"
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

    <VRow v-else-if="filteredProjects.length > 0">
      <VCol
        v-for="project in filteredProjects"
        :key="project._id"
        cols="12"
        sm="6"
        lg="4"
      >
        <VCard
          class="h-100 d-flex flex-column"
          elevation="2"
          hover
          @click="openProjectDialog(project)"
        >
          <VImg
            :src="getProjectImage(project)"
            height="200"
            cover
            class="bg-grey-lighten-2"
            gradient="to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.7)"
          >
            <VCardTitle class="text-white">{{ project.title }}</VCardTitle>
            <VCardSubtitle class="text-white">
              {{ project.company || 'Personal Project' }} • {{ formatDate(project.date) }}
            </VCardSubtitle>
          </VImg>
          
          <VCardText class="pt-4 flex-grow-1">
            <p class="text-body-2 text-medium-emphasis">
              {{ project.summary || (project.description ? project.description.substring(0, 150) + (project.description.length > 150 ? '...' : '') : 'No description available.') }}
            </p>
            
            <div v-if="project.highlights && project.highlights.length > 0" class="mt-2">
              <div v-for="(highlight, index) in project.highlights.slice(0, 2)" :key="index" class="d-flex align-start mb-1">
                <VIcon size="small" class="mr-2 mt-1" color="primary">mdi-check-circle</VIcon>
                <span class="text-caption">{{ highlight }}</span>
              </div>
            </div>
          </VCardText>
          
          <VCardActions class="px-4 pb-4">
            <VSpacer />
            <VBtn
              color="primary"
              variant="text"
              size="small"
              @click.stop="openProjectDialog(project)"
            >
              View Details
            </VBtn>
          </VCardActions>
        </VCard>
      </VCol>
    </VRow>

    <VRow v-else>
      <VCol cols="12" class="text-center py-12">
        <VIcon size="64" class="mb-4" color="grey-lighten-1">mdi-folder-open-outline</VIcon>
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
            <VIcon>mdi-close</VIcon>
          </VBtn>
        </VToolbar>
        
        <VImg
          :src="getProjectImage(selectedProject)"
          height="300"
          cover
          class="bg-grey-lighten-2"
        >
          <VRow class="fill-height align-end">
            <VCol cols="12" class="pa-6">
            </VCol>
          </VRow>
        </VImg>
        
        <VCardText class="pt-6">
          <div class="d-flex flex-wrap align-center gap-4 mb-4">
            <VChip v-if="selectedProject.company" color="primary" variant="flat" size="small">
              <VIcon start>mdi-domain</VIcon>
              {{ selectedProject.company }}
            </VChip>
            
            <VChip variant="outlined" size="small" v-if="selectedProject.duration">
              <VIcon start>mdi-calendar-range</VIcon>
              {{ selectedProject.duration }}
            </VChip>
            
            <VChip 
              v-else-if="selectedProject.date"
              variant="outlined" 
              size="small"
            >
              <VIcon start>mdi-calendar-month</VIcon>
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
                  <VIcon color="primary" size="small" class="mr-2">mdi-check-circle</VIcon>
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
            <VIcon start>mdi-open-in-new</VIcon>
            View Live
          </VBtn>
        </VCardActions>
      </VCard>
    </VDialog>
  </VContainer>
</template>

<style scoped>
.portfolio-container {
  max-width: 1400px;
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
