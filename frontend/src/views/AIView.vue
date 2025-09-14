<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import { useDisplay } from 'vuetify';
import axios from 'axios';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import {
  mdiRobot,
  mdiLightbulbOutline,
  mdiChat,
  mdiRefresh,
  mdiAccount,
  mdiSend,
  mdiPlus,
  mdiLoading
} from '@mdi/js';

const { mobile } = useDisplay();

// Chat state
const messages = ref([]);
const userInput = ref('');
const isTyping = ref(false);
const messagesContainer = ref(null);
const conversationId = ref(null);

// Sample welcome message
const welcomeMessage = {
  role: 'assistant',
  content: "Hello! I'm an AI assistant here to answer your questions about Rajorshi Tah's professional background, skills, and experience. What would you like to know?",
  timestamp: new Date()
};

// Suggested questions
const suggestedQuestions = [
  "What is Rajorshi's professional background?",
  "What programming languages does he know?",
  "Tell me about his work experience",
  "What are his key skills?",
  "What projects has he worked on?"
];

// Format message with markdown and sanitize HTML
const formatMessage = (content) => {
  if (!content) return '';
  const markdown = marked.parse(content);
  return DOMPurify.sanitize(markdown);
};

// Format time
const formatTime = (date) => {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

// Scroll to bottom of messages
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

// Send suggested question
const sendSuggestedQuestion = (question) => {
  userInput.value = question;
  sendMessage();
};

// Send message to the AI
const sendMessage = async () => {
  const message = userInput.value.trim();
  if (!message || isTyping.value) return;

  // Add user message to chat
  const userMessage = {
    role: 'user',
    content: message,
    timestamp: new Date()
  };
  messages.value.push(userMessage);
  userInput.value = '';
  
  // Scroll to bottom after user message is added
  scrollToBottom();
  
  // Show typing indicator
  isTyping.value = true;
  
  try {
    // Prepare request payload
    const payload = {
      question: message
    };
    
    // Add conversation_id if we have one (for continuing conversation)
    if (conversationId.value) {
      payload.conversation_id = conversationId.value;
    }
    
    // Send message to backend using new unified endpoint
    const response = await axios.post('/api/ai/chat/message', payload);
    
    // Store conversation_id for future messages
    if (response.data.conversation_id) {
      conversationId.value = response.data.conversation_id;
    }
    
    // Add AI response to chat
    const aiMessage = {
      role: 'assistant',
      content: response.data.answer,
      timestamp: new Date()
    };
    
    messages.value.push(aiMessage);
    
    // Save conversation after successful response
    saveConversation();
  } catch (error) {
    console.error('Error getting AI response:', error);
    
    // Add error message
    const errorMessage = {
      role: 'assistant',
      content: 'Sorry, I encountered an error while processing your request. Please try again later.',
      timestamp: new Date(),
      isError: true
    };
    
    messages.value.push(errorMessage);
  } finally {
    isTyping.value = false;
    scrollToBottom();
  }
};

// Clear chat
const clearChat = () => {
  messages.value = [welcomeMessage];
  conversationId.value = null; // Reset conversation ID for new chat
  localStorage.removeItem('ai_conversation'); // Clear saved conversation
  scrollToBottom();
};

// Save conversation to localStorage
const saveConversation = () => {
  if (conversationId.value && messages.value.length > 1) {
    const conversationData = {
      conversationId: conversationId.value,
      messages: messages.value,
      lastUpdated: new Date().toISOString()
    };
    localStorage.setItem('ai_conversation', JSON.stringify(conversationData));
  }
};

// Load conversation from localStorage
const loadConversation = () => {
  try {
    const saved = localStorage.getItem('ai_conversation');
    if (saved) {
      const conversationData = JSON.parse(saved);
      // Only load if conversation is less than 24 hours old
      const lastUpdated = new Date(conversationData.lastUpdated);
      const now = new Date();
      const hoursDiff = (now - lastUpdated) / (1000 * 60 * 60);
      
      if (hoursDiff < 24 && conversationData.conversationId) {
        conversationId.value = conversationData.conversationId;
        messages.value = conversationData.messages;
        return true;
      }
    }
  } catch (error) {
    console.error('Error loading conversation:', error);
  }
  return false;
};

// Initialize with welcome message or load saved conversation
onMounted(() => {
  const loaded = loadConversation();
  if (!loaded && messages.value.length === 0) {
    messages.value.push(welcomeMessage);
  }
  scrollToBottom();
});

// Watch for messages changes to scroll to bottom
watch(messages, () => {
  scrollToBottom();
}, { deep: true });
</script>

<template>
  <VContainer class="ai-container py-8">
    <!-- Suggested Questions (show only when no messages except welcome) -->
    <VRow v-if="messages.length <= 1" justify="center" class="mb-6">
      <VCol cols="12" md="8" lg="6">
        <VCard class="pa-4" elevation="1">
          <VCardTitle class="text-h6 mb-3">
            <VIcon :icon="mdiLightbulbOutline" class="mr-2" />
            Suggested Questions
          </VCardTitle>
          <div class="d-flex flex-wrap gap-2">
            <VChip
              v-for="(question, index) in suggestedQuestions"
              :key="index"
              color="primary"
              variant="outlined"
              size="small"
              @click="sendSuggestedQuestion(question)"
              class="text-caption"
            >
              {{ question }}
            </VChip>
          </div>
        </VCard>
      </VCol>
    </VRow>

    <!-- Chat Container -->
    <VRow justify="center" class="fill-height">
      <VCol cols="12" md="8" lg="6" class="fill-height">
        <VCard class="chat-container" elevation="4">
          <!-- Chat Header -->
          <VToolbar color="primary" class="elevation-0">
            <VToolbarTitle class="text-white d-flex align-center">
              <VIcon :icon="mdiChat" class="mr-2" size="x-large" />
              <span class="text-h6 font-weight-medium">AI Assistant</span>
            </VToolbarTitle>
            <VSpacer />
            <VBtn
              v-if="messages.length > 1"
              color="white"
              variant="outlined"
              :prepend-icon="mdiPlus"
              @click="clearChat"
              :loading="isTyping"
              class="text-none"
            >
              New Chat
            </VBtn>
          </VToolbar>

          <!-- Messages -->
          <VCardText class="messages pa-4" ref="messagesContainer">
            <template v-for="(message, index) in messages" :key="index">
              <div
                :class="[
                  'message',
                  message.role === 'user' ? 'user-message' : 'ai-message',
                  'mb-4',
                  'fade-in'
                ]"
              >
                <div class="message-content">
                  <div class="d-flex align-center mb-2">
                    <VAvatar size="32" :color="message.role === 'user' ? 'primary' : 'secondary'" class="mr-2">
                      <VIcon v-if="message.role === 'user'" :icon="mdiAccount" color="white" />
                      <VIcon v-else :icon="mdiRobot" color="white" />
                    </VAvatar>
                    <span class="text-caption font-weight-medium">
                      {{ message.role === 'user' ? 'You' : 'AI Assistant' }}
                    </span>
                    <VSpacer />
                    <span class="text-caption text-medium-emphasis">
                      {{ formatTime(message.timestamp) }}
                    </span>
                  </div>
                  <div class="message-text" v-html="formatMessage(message.content)"></div>
                </div>
              </div>
            </template>

            <!-- Typing indicator -->
            <div v-if="isTyping" class="typing-indicator mb-4">
              <div class="d-flex align-center">
                <VAvatar size="32" color="secondary" class="mr-2">
                  <VIcon :icon="mdiRobot" color="white" />
                </VAvatar>
                <div class="typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </VCardText>

          <!-- Input Area -->
          <VCardActions class="px-4 pb-4 pt-2 bg-grey-lighten-5">
            <VForm @submit.prevent="sendMessage" class="w-100">
              <div class="position-relative">
                <VTextarea
                  v-model="userInput"
                  label="Ask me anything about Rajorshi..."
                  variant="solo"
                  rows="1"
                  auto-grow
                  hide-details
                  :disabled="isTyping"
                  :loading="isTyping"
                  @keydown.enter.exact.prevent="sendMessage"
                  class="message-input elevation-1"
                  bg-color="white"
                  rounded="lg"
                >
                  <template v-slot:append-inner>
                    <VBtn
                      :disabled="!userInput.trim() || isTyping"
                      :loading="isTyping"
                      icon
                      color="primary"
                      variant="flat"
                      size="small"
                      @click="sendMessage"
                      class="send-btn elevation-2"
                      :class="{ 'mr-1': isTyping }"
                    >
                      <VIcon :icon="isTyping ? mdiLoading : mdiSend" />
                    </VBtn>
                  </template>
                </VTextarea>
                <div class="text-caption text-medium-emphasis mt-3 text-center d-flex align-center justify-center">
                  <VIcon :icon="mdiLightbulbOutline" size="small" class="mr-1" />
                  <span>Ask about work experience, skills, or projects</span>
                </div>
              </div>
            </VForm>
          </VCardActions>
        </VCard>
      </VCol>
    </VRow>
  </VContainer>
</template>

<style scoped>
.ai-container {
  max-width: 1500px;
  margin: 0 auto;
  padding: 0 24px;
}

.chat-container {
  border-radius: 16px;
  overflow: hidden;
  height: 70vh;
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.message {
  max-width: 85%;
  margin-left: 0;
  margin-right: auto;
  animation: fadeIn 0.3s ease;
}

.user-message {
  margin-left: auto;
  margin-right: 0;
}

.user-message .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 18px 18px 4px 18px;
  padding: 12px 16px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.ai-message .message-content {
  background: white;
  color: #333;
  border-radius: 18px 18px 18px 4px;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message-text {
  line-height: 1.6;
  word-wrap: break-word;
}

.message-text :deep(p) {
  margin-bottom: 8px;
}

.message-text :deep(a) {
  color: #1976d2;
  text-decoration: none;
}

.message-text :deep(a:hover) {
  text-decoration: underline;
}

.message-text :deep(ul),
.message-text :deep(ol) {
  padding-left: 20px;
  margin: 8px 0;
}

.message-text :deep(li) {
  margin-bottom: 4px;
}

.message-text :deep(code) {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 2px 4px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.9em;
}

.typing-indicator {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: white;
  border-radius: 18px;
  width: fit-content;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.typing-dots {
  display: flex;
  align-items: center;
  height: 24px;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  margin: 0 2px;
  background-color: #666;
  border-radius: 50%;
  display: inline-block;
  opacity: 0.4;
}

.typing-dots span:nth-child(1) {
  animation: typing 1s infinite;
}

.typing-dots span:nth-child(2) {
  animation: typing 1s infinite 0.2s;
}

.typing-dots span:nth-child(3) {
  animation: typing 1s infinite 0.4s;
}

@keyframes typing {
  0%, 100% {
    opacity: 0.4;
    transform: translateY(0);
  }
  50% {
    opacity: 1;
    transform: translateY(-4px);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Custom scrollbar */
.messages::-webkit-scrollbar {
  width: 6px;
}

.messages::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

.messages::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.messages::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

.v-chip {
  cursor: pointer;
  transition: all 0.2s ease;
}

.v-chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Responsive adjustments */
@media (max-width: 960px) {
  .chat-container {
    height: 75vh;
  }
}

@media (max-width: 600px) {
  .ai-container {
    padding: 16px 8px;
  }
  
  .chat-container {
    height: 80vh;
  }
  
  .message {
    max-width: 90%;
  }
}
</style>
