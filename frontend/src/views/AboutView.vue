<template>
  <v-container class="about-container">
    <v-row>
      <v-col cols="12" md="8" offset-md="2">
        <v-card class="pa-6">
          <v-card-title class="text-h4 mb-6">About Me</v-card-title>
          
          <v-row>
            <v-col cols="12" md="4" class="text-center">
              <v-avatar size="200" class="mb-4">
                <v-img
                  :src="profilePictureUrl"
                  alt="Rajorshi Tah"
                  class="elevation-6"
                >
                  <template v-slot:error>
                    <v-icon size="100" color="grey-lighten-1">mdi-account-circle</v-icon>
                  </template>
                </v-img>
              </v-avatar>
              
              <div class="text-h6 font-weight-bold mb-2">Rajorshi Tah</div>
              <div class="text-subtitle-1 text-medium-emphasis mb-4">
                Software Developer | AI/ML Engineer
              </div>
              
              <div class="d-flex justify-center gap-4">
                <v-btn
                  v-for="icon in socialIcons"
                  :key="icon.icon"
                  :href="icon.link"
                  target="_blank"
                  rel="noopener"
                  :icon="icon.icon"
                  variant="text"
                  size="small"
                  color="primary"
                ></v-btn>
              </div>
            </v-col>
            
            <v-col cols="12" md="8">
              <div class="text-body-1 mb-6">
                <p class="mb-4">
                  Hello! I'm Rajorshi Tah, a passionate software developer with expertise in backend systems, 
                  AI/ML, and full-stack development. I currently work at Accenture, where I build scalable 
                  applications that solve real-world problems.
                </p>
                
                <p class="mb-4">
                  With several years of experience in the tech industry, I've had the opportunity to work on 
                  a variety of projects, from small startups to large enterprise applications. My technical 
                  skills span across multiple programming languages and frameworks, allowing me to adapt to 
                  different project requirements and deliver high-quality solutions.
                </p>
                
                <p class="mb-4">
                  When I'm not coding, you can find me exploring new technologies, contributing to open-source 
                  projects, or sharing my knowledge through blog posts and talks. I'm always excited about 
                  learning new things and collaborating with like-minded individuals.
                </p>
              </div>
              
              <v-divider class="my-6"></v-divider>
              
              <div class="mb-6">
                <div class="text-h6 mb-4">Technical Skills</div>
                <v-chip
                  v-for="(skills, category) in skillsByCategory"
                  :key="category"
                  class="ma-1"
                  color="primary"
                  variant="outlined"
                  :prepend-icon="skillIcons[category]"
                >
                  {{ category }}
                </v-chip>
              </div>
              
              <v-btn
                color="primary"
                variant="outlined"
                href="/cv"
                class="mr-4"
              >
                <v-icon start>mdi-file-account</v-icon>
                View My CV
              </v-btn>
              
              <v-btn
                color="primary"
                href="#contact"
              >
                <v-icon start>mdi-email</v-icon>
                Contact Me
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const authStore = useAuthStore()
const profileData = ref(null)

const socialIcons = [
  { icon: 'mdi-github', link: 'https://github.com/rajorshi' },
  { icon: 'mdi-linkedin', link: 'https://linkedin.com/in/rajorshi-tah' },
  { icon: 'mdi-twitter', link: 'https://twitter.com/rajorshitah' },
];

const profilePictureUrl = computed(() => {
  if (profileData.value?.profile_picture && profileData.value.profile_picture !== '/api/profile/picture') {
    return `${axios.defaults.baseURL}${profileData.value.profile_picture}`
  }
  return 'https://via.placeholder.com/200?text=No+Image'
})

const fetchProfileData = async () => {
  try {
    const response = await axios.get('/api/profile')
    profileData.value = response.data
  } catch (error) {
    console.error('Failed to fetch profile data:', error)
  }
}

onMounted(() => {
  fetchProfileData()
})

const skillsByCategory = {
  'Programming': ['Python', 'JavaScript', 'Node.js', 'C++', 'SQL'],
  'Backend': ['Flask', 'Django', 'Express.js', 'RESTful APIs', 'GraphQL'],
  'Databases': ['MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'InfluxDB'],
  'AI/ML': ['TensorFlow', 'PyTorch', 'NLP', 'Computer Vision', 'LLMs'],
  'DevOps': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Terraform'],
  'Frontend': ['Vue.js', 'React', 'TypeScript', 'Vuetify', 'Tailwind CSS']
};

const skillIcons = {
  'Programming': 'mdi-code-braces',
  'Backend': 'mdi-server',
  'Databases': 'mdi-database',
  'AI/ML': 'mdi-brain',
  'DevOps': 'mdi-application-cog',
  'Frontend': 'mdi-monitor'
};
</script>

<style scoped>
.about-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px;
}
</style>
