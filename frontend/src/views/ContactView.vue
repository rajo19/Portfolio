<template>
  <v-container class="contact-container">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="pa-6">
          <v-card-title class="text-h4 mb-6">Get In Touch</v-card-title>
          
          <v-form @submit.prevent="submitForm" v-model="isFormValid">
            <v-text-field
              v-model="form.name"
              label="Name"
              :rules="[v => !!v || 'Name is required']"
              required
              variant="outlined"
              class="mb-4"
            ></v-text-field>
            
            <v-text-field
              v-model="form.email"
              label="Email"
              :rules="[
                v => !!v || 'Email is required',
                v => /.+@.+\..+/.test(v) || 'Email must be valid'
              ]"
              required
              variant="outlined"
              class="mb-4"
            ></v-text-field>
            
            <v-text-field
              v-model="form.subject"
              label="Subject"
              :rules="[v => !!v || 'Subject is required']"
              required
              variant="outlined"
              class="mb-4"
            ></v-text-field>
            
            <v-textarea
              v-model="form.message"
              label="Message"
              :rules="[v => !!v || 'Message is required']"
              required
              variant="outlined"
              rows="5"
              class="mb-6"
            ></v-textarea>
            
            <v-btn
              type="submit"
              color="primary"
              size="large"
              :loading="loading"
              :disabled="!isFormValid || loading"
            >
              Send Message
            </v-btn>
          </v-form>
        </v-card>
        
        <v-card class="mt-6 pa-6" variant="outlined">
          <v-card-title class="text-h5 mb-4">Contact Information</v-card-title>
          
          <v-list lines="two" class="bg-transparent">
            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-email" class="me-4"></v-icon>
              </template>
              <v-list-item-title>Email</v-list-item-title>
              <v-list-item-subtitle>rajorshitah9@gmail.com</v-list-item-subtitle>
            </v-list-item>
            
            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-phone" class="me-4"></v-icon>
              </template>
              <v-list-item-title>Phone</v-list-item-title>
              <v-list-item-subtitle>(+81) 80-4817-2852 | (+91) 94748-06123</v-list-item-subtitle>
            </v-list-item>
            
            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-map-marker" class="me-4"></v-icon>
              </template>
              <v-list-item-title>Location</v-list-item-title>
              <v-list-item-subtitle>Tokyo, Japan 136-0073</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
    
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const form = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
});

const isFormValid = ref(false);
const loading = ref(false);
const snackbar = ref({
  show: false,
  message: '',
  color: 'success'
});

const submitForm = async () => {
  if (!isFormValid.value) return;
  
  loading.value = true;
  
  try {
    await axios.post('/api/contact', form.value);
    
    // Reset form
    form.value = {
      name: '',
      email: '',
      subject: '',
      message: ''
    };
    
    // Show success message
    snackbar.value = {
      show: true,
      message: 'Your message has been sent successfully!',
      color: 'success'
    };
  } catch (error) {
    console.error('Error sending message:', error);
    
    // Show error message
    snackbar.value = {
      show: true,
      message: 'Failed to send message. Please try again later.',
      color: 'error'
    };
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.contact-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px;
}
</style>
