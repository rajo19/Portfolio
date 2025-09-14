<template>
  <v-container class="blog-editor">
    <v-card>
      <v-toolbar color="primary" dark>
        <v-toolbar-title>{{ isEditing ? 'Edit Post' : 'New Post' }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="$router.go(-1)">
          <v-icon :icon="mdiClose" />
        </v-btn>
      </v-toolbar>
      
      <v-card-text class="pa-6">
        <v-form v-model="isFormValid" @submit.prevent="savePost">
          <v-text-field
            v-model="postForm.title"
            label="Title"
            variant="outlined"
            :rules="[v => !!v || 'Title is required']"
            class="mb-4"
            required
          ></v-text-field>
          
          <v-text-field
            v-model="postForm.image"
            label="Featured Image URL"
            variant="outlined"
            class="mb-4"
            hint="Optional. URL of the featured image"
            persistent-hint
          ></v-text-field>
          
          <v-combobox
            v-model="postForm.tags"
            label="Tags"
            variant="outlined"
            multiple
            chips
            closable-chips
            class="mb-4"
            hint="Press enter or comma to add a tag"
            persistent-hint
          ></v-combobox>
          
          <div class="d-flex align-center mb-2">
            <label class="text-subtitle-2 font-weight-medium">Content</label>
            <v-spacer></v-spacer>
            <v-btn-toggle
              v-model="editorMode"
              mandatory
              density="compact"
              variant="outlined"
            >
              <v-btn value="edit" size="small">
                <v-icon :icon="mdiPencil" size="small" class="mr-1" />
                Edit
              </v-btn>
              <v-btn value="preview" size="small">
                <v-icon :icon="mdiEye" size="small" class="mr-1" />
                Preview
              </v-btn>
            </v-btn-toggle>
          </div>
          
          <v-card v-if="editorMode === 'preview'" variant="outlined" class="mb-4 pa-4" style="min-height: 300px;">
            <div class="markdown-preview" v-html="formatMarkdown(postForm.content)"></div>
          </v-card>
          
          <v-textarea
            v-else
            v-model="postForm.content"
            label="Write your post in Markdown"
            variant="outlined"
            :rules="[v => !!v || 'Content is required']"
            rows="15"
            auto-grow
            class="mb-4"
            required
          ></v-textarea>
          
          <v-divider class="my-4"></v-divider>
          
          <div class="d-flex justify-space-between">
            <v-btn
              color="secondary"
              variant="text"
              @click="$router.go(-1)"
              :disabled="saving"
            >
              Cancel
            </v-btn>
            
            <div>
              <v-btn
                color="primary"
                type="submit"
                :loading="saving"
                :disabled="!isFormValid || saving"
              >
                {{ isEditing ? 'Update Post' : 'Publish Post' }}
              </v-btn>
            </div>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import {
  mdiClose,
  mdiPencil,
  mdiEye
} from '@mdi/js'

const route = useRoute()
const router = useRouter()

const isEditing = computed(() => !!route.params.id)
const isFormValid = ref(false)
const editorMode = ref('edit')
const saving = ref(false)

const postForm = ref({
  title: '',
  content: '',
  tags: [],
  image: '',
  published: true
})

const formatMarkdown = (content) => {
  if (!content) return ''
  const markdown = marked.parse(content)
  return DOMPurify.sanitize(markdown)
}

const savePost = async () => {
  if (!isFormValid.value) return
  
  saving.value = true
  
  try {
    if (isEditing.value) {
      await axios.put(`/api/blog/${route.params.id}`, postForm.value)
    } else {
      await axios.post('/api/blog', postForm.value)
    }
    
    router.push({ name: 'blog' })
  } catch (error) {
    console.error('Error saving post:', error)
  } finally {
    saving.value = false
  }
}

const fetchPost = async () => {
  if (!isEditing.value) return
  
  try {
    const response = await axios.get(`/api/blog/${route.params.id}`)
    const { title, content, tags, image } = response.data
    
    postForm.value = {
      title,
      content,
      tags: [...(tags || [])],
      image: image || ''
    }
  } catch (error) {
    console.error('Error fetching post:', error)
    router.push({ name: 'blog' })
  }
}

onMounted(() => {
  fetchPost()
})
</script>

<style scoped>
.blog-editor {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 16px;
}

.markdown-preview {
  line-height: 1.8;
}
</style>
