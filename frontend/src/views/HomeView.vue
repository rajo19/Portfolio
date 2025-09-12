<script setup>
import { useDisplay } from 'vuetify';
import { ref, onMounted } from 'vue';
import axios from 'axios';

const { mobile } = useDisplay();

// Social media links with logos
const socialIcons = [
  { 
    icon: 'mdi-github', 
    logo: 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg',
    link: 'https://github.com/rajorshitah', 
    color: 'grey-darken-4', 
    label: 'GitHub' 
  },
  { 
    icon: 'mdi-linkedin', 
    logo: 'https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg',
    link: 'https://www.linkedin.com/in/rajorshi-tah', 
    color: 'blue-darken-1', 
    label: 'LinkedIn' 
  },
  { 
    icon: 'mdi-instagram', 
    logo: 'https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png',
    link: 'https://instagram.com/rajorshitah', 
    color: 'pink', 
    label: 'Instagram' 
  },
  { 
    icon: 'mdi-twitter', 
    logo: 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/twitter/twitter-original.svg',
    link: 'https://twitter.com/rajorshitah', 
    color: 'light-blue', 
    label: 'Twitter' 
  },
];

// Import Material Design Icons
import { mdiBriefcase, mdiPost, mdiEmail } from '@mdi/js';

// Navigation links with SVG icons
const navLinks = [
  { 
    title: 'Portfolio', 
    to: '/portfolio', 
    icon: mdiBriefcase,
    color: 'deep-purple',
    hoverColor: 'deep-purple-darken-1'
  },
  { 
    title: 'Blog', 
    to: '/blog', 
    icon: mdiPost,
    color: 'light-blue',
    hoverColor: 'light-blue-darken-1'
  },
  { 
    title: 'Contact', 
    to: '/contact', 
    icon: mdiEmail,
    color: 'teal',
    hoverColor: 'teal-darken-1'
  },
];

const profilePictureUrl = ref('https://via.placeholder.com/300?text=Loading...');

const loadProfilePicture = async () => {
  try {
    console.log('Attempting to load profile picture...');
    
    // First check if we have a default image to show while loading
    profilePictureUrl.value = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiB2aWV3Qm94PSIwIDAgMzAwIDMwMCI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iI2VlZSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5Mb2FkaW5nLi4uPC90ZXh0Pjwvc3ZnPg=';
    
    // Try to get the latest profile picture
    const response = await axios.get('/api/profile/profile_pic', {
      responseType: 'blob',
      validateStatus: status => status < 500 // Don't throw for 404
    });
    
    console.log('Received response with status:', response.status);
    
    if (response.status === 200 && response.data) {
      // Create a local URL for the image blob
      const imageUrl = URL.createObjectURL(response.data);
      console.log('Created blob URL:', imageUrl);
      
      // Create an image element to verify the image loads
      const img = new Image();
      img.onload = () => {
        console.log('Image loaded successfully');
        profilePictureUrl.value = imageUrl;
      };
      img.onerror = () => {
        console.error('Failed to load the image');
        throw new Error('Failed to load image');
      };
      img.src = imageUrl;
    } else {
      throw new Error('No profile picture available');
    }
    
  } catch (error) {
    console.error('Error loading profile picture:', error.message);
    // Fallback to a default profile picture
    profilePictureUrl.value = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiB2aWV3Qm94PSIwIDAgMzAwIDMwMCI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iI2VlZSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5ObyBQcm9maWxlIFBpY3R1cmU8L3RleHQ+PC9zdmc+';
  }
};

const handleImageError = (event) => {
  console.error('Error loading profile image, using fallback');
  // Use the same inline SVG as the fallback
  profilePictureUrl.value = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiB2aWV3Qm94PSIwIDAgMzAwIDMwMCI+CiAgPHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iI2VlZSIvPgogIDx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5FcnJvciBMb2FkaW5nIEltYWdlPC90ZXh0Pgo8L3N2Zz4=';
  if (event?.target) {
    event.target.src = profilePictureUrl.value;
  }
};

// Load the profile picture when the component mounts
onMounted(() => {
  loadProfilePicture();
});
</script>

<template>
  <VContainer class="home-container d-flex align-center justify-center" style="min-height: 80vh;">
    <VRow align="center" justify="center" class="fill-height">
      <!-- Profile Picture -->
      <VCol cols="12" md="5" class="text-center">
        <div class="profile-avatar-container">
          <div class="profile-avatar">
            <img
              :src="profilePictureUrl"
              alt="Rajorshi Tah"
              class="profile-image"
              @error="handleImageError"
            >
          </div>
        </div>
      </VCol>

      <!-- Content -->
      <VCol cols="12" md="7" class="text-center text-md-start">
        <h1 class="text-h3 text-md-h2 font-weight-bold mb-4">
          Hi, I'm <span class="text-primary">Rajorshi Tah</span>
        </h1>
        <h2 class="text-h5 text-md-h4 text-medium-emphasis mb-6">
          Full Stack Developer & AI Engineer
        </h2>
        <p class="text-body-1 mb-8">
          Experienced Full Stack Developer with a passion for building intelligent applications. 
          I specialize in creating seamless digital experiences using modern web technologies 
          and artificial intelligence to solve complex problems.
        </p>
        
        <!-- Navigation Links -->
        <div class="d-flex flex-wrap justify-center justify-md-start gap-3 mb-8">
          <VBtn
            v-for="(item, index) in navLinks"
            :key="index"
            :to="item.to"
            variant="flat"
            size="large"
            rounded="pill"
            class="nav-button"
            :color="item.color"
            elevation="2"
          >
            <VIcon :icon="item.icon" class="mr-2" />
            {{ item.title }}
          </VBtn>
        </div>

        <!-- AI Assistant Button -->
        <div class="d-flex justify-center justify-md-start gap-4 mb-8">
          <RouterLink 
            to="/ai-assistant" 
            class="ai-assistant-btn"
          >
            <span class="magic-icon">✨</span>
            <span class="ml-2">AI Assistant</span>
          </RouterLink>
        </div>

        <!-- Social Links -->
        <div class="social-links d-flex justify-center justify-md-start">
          <VTooltip
            v-for="(social, index) in socialIcons"
            :key="index"
            :text="social.label"
            location="bottom"
          >
            <template v-slot:activator="{ props }">
              <a
                v-bind="props"
                :href="social.link"
                target="_blank"
                rel="noopener"
                class="social-icon"
                style="outline: none;"
              >
                <VImg
                  :src="social.logo"
                  :alt="social.label"
                  width="28"
                  height="28"
                  contain
                />
              </a>
            </template>
          </VTooltip>
        </div>
      </VCol>
    </VRow>
  </VContainer>
</template>

<style scoped>
.profile-avatar-container {
  width: 300px;
  height: 300px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid #f5f5f5;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  background: #f5f5f5;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-avatar {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  border-radius: 50%;
  background: #f5f5f5;
}

.profile-avatar img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.3s ease;
  border-radius: 50%;
  border: 6px solid #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: scale(1.1);
  box-sizing: border-box;
}
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-image {
  border: 6px solid #f5f5f5;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.profile-image:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.social-links {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  justify-content: center;
  margin-top: 1.5rem;
  padding: 0 4px;
}

.social-icon {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  opacity: 0.8;
  cursor: pointer;
  outline: none !important;
  -webkit-tap-highlight-color: transparent;
  -webkit-focus-ring-color: transparent;
}

.social-icon:hover {
  transform: scale(1.3);
  opacity: 1;
  box-shadow: 0 0px 20px rgba(154, 31, 31, 0.15);
}

.instagram-gradient {
  background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
  color: white !important;
}

.ai-assistant-btn {
  background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%);
  color: white !important;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: none;
  padding: 0 24px;
  height: 48px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(110, 142, 251, 0.4);
}

.ai-assistant-btn :deep(.v-btn__prepend) {
  margin-inline-end: 8px;
  margin-inline-start: -4px;
}

.ai-assistant-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none !important;
  cursor: pointer;
  outline: none;
  border: none;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
  position: relative;
  white-space: nowrap;
  text-transform: none;
  letter-spacing: 0.5px;
  font-weight: 600;
  font-size: 0.9375rem;
  line-height: 1.5;
  border-radius: 9999px;
  padding: 0 24px;
  height: 48px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%);
  color: white !important;
  box-shadow: 0 4px 15px rgba(110, 142, 251, 0.4);
  position: relative;
  overflow: hidden;
}

.ai-assistant-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(110, 142, 251, 0.5);
  text-decoration: none !important;
}

/* Navigation Buttons */
.nav-button {
  text-transform: none;
  letter-spacing: 0.5px;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 140px;
  padding: 0 24px;
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1), 
              0 4px 5px 0 rgba(0, 0, 0, 0.08), 
              0 1px 10px 0 rgba(0, 0, 0, 0.06) !important;
}

.nav-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px -1px rgba(0, 0, 0, 0.15), 
              0 6px 10px 0 rgba(0, 0, 0, 0.12), 
              0 1px 20px 0 rgba(0, 0, 0, 0.1) !important;
}

/* Specific button colors */
.nav-button.v-btn--variant-flat.v-theme--light {
  color: white;
}

.nav-button.deep-purple {
  background: linear-gradient(135deg, #7E57C2 0%, #5E35B1 100%);
}

.nav-button.light-blue {
  background: linear-gradient(135deg, #29B6F6 0%, #0288D1 100%);
}

.nav-button.teal {
  background: linear-gradient(135deg, #26A69A 0%, #00897B 100%);
}

/* AI Assistant Button */
.ai-assistant-btn {
  position: relative;
  overflow: hidden;
  padding-left: 20px !important;
  padding-right: 24px !important;
  min-width: 160px;
  letter-spacing: 0.5px;
  text-transform: none;
  font-weight: 500;
}

.magic-icon {
  display: inline-block;
  font-size: 20px;
  margin-right: 8px;
  animation: float 3s ease-in-out infinite;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-5px) rotate(10deg); }
}

.ai-assistant-btn:hover .magic-icon {
  animation: sparkle 1s infinite, float 3s ease-in-out infinite;
}

@keyframes sparkle {
  0% { filter: drop-shadow(0 0 4px rgba(255, 215, 0, 0.7)); }
  50% { filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.9)) brightness(1.2); }
  100% { filter: drop-shadow(0 0 4px rgba(255, 215, 0, 0.7)); }
}

.social-icon:hover {
  transform: translateY(-3px);
  background-color: #e9ecef;
}

.v-btn--size-large {
  min-width: 140px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.text-primary {
  background: linear-gradient(45deg, #1976d2, #21c1d6);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

@media (max-width: 960px) {
  .home-container {
    padding: 1rem;
  }
  
  .v-avatar {
    width: 250px !important;
    height: 250px !important;
  }
  
  h1 {
    font-size: 2rem !important;
  }
  
  h2 {
    font-size: 1.5rem !important;
  }
}
</style>
