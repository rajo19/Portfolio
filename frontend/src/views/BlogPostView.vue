<template>
  <v-container class="blog-post-container">
    <v-btn
      v-if="!$vuetify.display.mobile"
      color="secondary"
      variant="text"
      :prepend-icon="mdiArrowLeft"
      @click="$router.go(-1)"
      class="mb-4"
    >
      Back to Blog
    </v-btn>
    
    <v-row v-if="!loading">
      <v-col cols="12" class="text-center">
        <v-chip color="primary" variant="outlined" class="mb-4">
          {{ formatDate(post.createdAt, 'long') }}
        </v-chip>
        <h1 class="text-h3 font-weight-bold mb-4">{{ post.title }}</h1>
        
        <div class="d-flex align-center justify-center mb-8">
          <v-avatar size="40" color="primary" class="mr-2">
            <v-icon :icon="mdiAccount" />
          </v-avatar>
          <span class="text-body-1">By {{ post.author || 'Admin' }}</span>
          
          <v-divider vertical class="mx-4"></v-divider>
          
          <div class="d-flex align-center">
            <v-icon :icon="mdiTagOutline" size="small" class="mr-1" />
            <div>
              <v-chip
                v-for="(tag, index) in post.tags"
                :key="index"
                size="small"
                color="primary"
                variant="outlined"
                class="mr-1 mb-1"
              >
                {{ tag }}
              </v-chip>
            </div>
          </div>
        </div>
        
        <v-img
          v-if="post.image"
          :src="post.image"
          height="400"
          cover
          class="rounded-lg mb-8"
        ></v-img>
        
        <v-card variant="text" class="text-left mb-8">
          <v-card-text>
            <div class="markdown-content" v-html="formatMarkdown(post.content)"></div>
          </v-card-text>
        </v-card>
        
        <v-divider class="my-8"></v-divider>
        
        <div class="d-flex justify-space-between align-center">
          <v-btn
            v-if="isAuthenticated"
            color="primary"
            variant="outlined"
            :prepend-icon="mdiPencil"
            @click="editPost"
          >
            Edit Post
          </v-btn>
          <div v-else></div>
          
          <v-btn
            color="primary"
            variant="text"
            :prepend-icon="mdiShareVariant"
            @click="sharePost"
          >
            Share
          </v-btn>
        </div>
      </v-col>
    </v-row>
    
    <v-row v-else>
      <v-col cols="12">
        <v-skeleton-loader type="article, actions"></v-skeleton-loader>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { useAuthStore } from '../stores/auth'
import {
  mdiArrowLeft,
  mdiAccount,
  mdiTagOutline,
  mdiPencil,
  mdiShareVariant
} from '@mdi/js'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = authStore.isAuthenticated

const post = ref({
  title: '',
  content: '',
  tags: [],
  image: '',
  author: 'Rajorshi Tah',
  createdAt: new Date().toISOString()
})

const loading = ref(true)

// Format date
const formatDate = (dateString, format = 'short') => {
  if (!dateString) return ''
  const date = new Date(dateString)
  
  if (format === 'long') {
    const options = { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }
    return date.toLocaleDateString(undefined, options)
  }
  
  // Short format
  return date.toLocaleDateString()
}

// Format markdown to HTML
const formatMarkdown = (content) => {
  if (!content) return ''
  const markdown = marked.parse(content)
  return DOMPurify.sanitize(markdown)
}

// Edit post
const editPost = () => {
  router.push({ 
    name: 'blog-edit', 
    params: { id: route.params.id } 
  })
}

// Share post
const sharePost = async () => {
  try {
    if (navigator.share) {
      await navigator.share({
        title: post.value.title,
        text: post.value.title,
        url: window.location.href
      })
    } else {
      // Fallback for browsers that don't support Web Share API
      await navigator.clipboard.writeText(window.location.href)
      alert('Link copied to clipboard!')
    }
  } catch (error) {
    console.error('Error sharing:', error)
  }
}

// Fetch blog post
const fetchPost = async () => {
  try {
    loading.value = true
    const response = await axios.get(`/api/blog/${route.params.id}`)
    post.value = response.data
  } catch (error) {
    console.error('Error fetching blog post:', error)
    router.push({ name: 'blog' })
  } finally {
    loading.value = false
  }
}

// Initialize
onMounted(() => {
  fetchPost()
})
</script>

<style scoped>
.blog-post-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 64px 16px;
}

.markdown-content {
  line-height: 1.8;
  font-size: 1.1rem;
  color: rgba(0, 0, 0, 0.87);
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
  margin: 1.5em 0 0.8em;
  line-height: 1.3;
}

.markdown-content :deep(h1) {
  font-size: 2em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-content :deep(h2) {
  font-size: 1.5em;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 0.3em;
}

.markdown-content :deep(h3) {
  font-size: 1.25em;
}

.markdown-content :deep(p) {
  margin: 0 0 1.5em;
  line-height: 1.8;
}

.markdown-content :deep(a) {
  color: #1976d2;
  text-decoration: none;
  font-weight: 500;
}

.markdown-content :deep(a:hover) {
  text-decoration: underline;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 2em;
  margin: 0 0 1.5em;
}

.markdown-content :deep(li) {
  margin-bottom: 0.5em;
}

.markdown-content :deep(code) {
  font-family: 'Courier New', Courier, monospace;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-size: 0.9em;
}

.markdown-content :deep(pre) {
  background-color: #f6f8fa;
  border-radius: 6px;
  padding: 16px;
  overflow: auto;
  margin: 0 0 1.5em;
}

.markdown-content :deep(pre code) {
  background: none;
  padding: 0;
  border-radius: 0;
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid #1976d2;
  margin: 1.5em 0;
  padding: 0.5em 1em;
  color: #666;
  background-color: #f9f9f9;
}

.markdown-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  margin: 1.5em 0;
}

.markdown-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1.5em 0;
  display: block;
  overflow-x: auto;
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
  border: 1px solid #ddd;
  padding: 8px 12px;
  text-align: left;
}

.markdown-content :deep(th) {
  background-color: #f5f5f5;
  font-weight: 600;
}

/* Responsive adjustments */
@media (max-width: 960px) {
  .blog-post-container {
    padding: 48px 16px;
  }
  
  .markdown-content {
    font-size: 1rem;
  }
}

@media (max-width: 600px) {
  .blog-post-container {
    padding: 32px 12px;
  }
  
  .markdown-content {
    font-size: 0.95rem;
  }
  
  .markdown-content :deep(h1) {
    font-size: 1.8em;
  }
  
  .markdown-content :deep(h2) {
    font-size: 1.4em;
  }
  
  .markdown-content :deep(h3) {
    font-size: 1.2em;
  }
}
</style>
