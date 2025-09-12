<template>
  <v-container class="blog-container">
    <v-row>
      <v-col cols="12" class="text-center">
        <h1 class="text-h3 font-weight-bold mb-2">Blog</h1>
        <p class="text-body-1 text-medium-emphasis mb-8">
          Thoughts, tutorials, and updates on my latest projects
        </p>
      </v-col>
    </v-row>

    <!-- Create New Post Button (Admin Only) -->
    <v-row v-if="isAuthenticated" class="mb-6">
      <v-col cols="12" class="text-end">
        <v-btn color="primary" prepend-icon="mdi-plus" @click="openEditor()">
          New Post
        </v-btn>
      </v-col>
    </v-row>

    <!-- Blog Posts Grid -->
    <v-row v-if="!loading">
      <v-col v-for="post in posts" :key="post._id" cols="12" md="6" lg="4">
        <v-card class="h-100 d-flex flex-column" hover>
          <v-img
            :src="post.image || 'https://via.placeholder.com/600x400?text=Blog+Post'"
            height="200"
            cover
            class="align-end"
            gradient="to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.7)"
          >
            <v-card-title class="text-white">{{ post.title }}</v-card-title>
            <v-card-subtitle class="text-white d-flex align-center">
              <v-icon small color="white" class="mr-1">mdi-account</v-icon>
              {{ post.author }}
              <v-icon small color="white" class="mx-2">mdi-circle-small</v-icon>
              <v-icon small color="white" class="mr-1">mdi-calendar</v-icon>
              {{ formatDate(post.createdAt) }}
            </v-card-subtitle>
          </v-img>
          
          <v-card-text class="flex-grow-1">
            <div class="d-flex flex-wrap gap-1 mb-3">
              <v-chip v-for="(tag, index) in post.tags.slice(0, 3)" :key="index" size="small" color="primary" variant="outlined" class="text-caption">
                {{ tag }}
              </v-chip>
            </div>
            <p class="text-body-2 mb-4">{{ getExcerpt(post.content) }}</p>
          </v-card-text>
          
          <v-card-actions class="px-4 pb-4">
            <v-spacer></v-spacer>
            <v-btn color="primary" variant="text" @click="viewPost(post._id)">
              Read More
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      
      <v-col v-if="posts.length === 0" cols="12" class="text-center py-12">
        <v-icon size="64" class="mb-4">mdi-post-outline</v-icon>
        <h3 class="text-h6">No blog posts yet</h3>
      </v-col>
    </v-row>
    
    <v-row v-else>
      <v-col v-for="i in 6" :key="i" cols="12" md="6" lg="4">
        <v-skeleton-loader type="image, article, actions"></v-skeleton-loader>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = authStore.isAuthenticated

// Blog posts
const posts = ref([])
const loading = ref(true)

// Format date
const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

// Get excerpt from content
const getExcerpt = (content, length = 150) => {
  if (!content) return ''
  const plainText = content
    .replace(/[#*_`\[\]()]/g, '')
    .replace(/<[^>]*>/g, '')
    .replace(/\s+/g, ' ')
    .trim()
  
  return plainText.length > length 
    ? plainText.substring(0, length) + '...' 
    : plainText
}

// Open post editor
const openEditor = (post = null) => {
  // Implementation for opening editor
  console.log('Open editor for post:', post)
}

// View single post
const viewPost = (postId) => {
  router.push({ name: 'blog-post', params: { id: postId } })
}

// Fetch blog posts
const fetchPosts = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/blog')
    posts.value = response.data
  } catch (error) {
    console.error('Error fetching blog posts:', error)
  } finally {
    loading.value = false
  }
}

// Initialize
onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.blog-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 64px 16px;
}

.v-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-radius: 8px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.v-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}

.v-card-text {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
</style>
