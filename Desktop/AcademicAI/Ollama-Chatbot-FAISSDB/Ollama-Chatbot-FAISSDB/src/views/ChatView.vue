<template>
  <div class="chat-view-container">
    <div class="chat-header">
      <h3>Chatbot</h3>
    </div>
    <div class="chat-layout">
      <div class="chat-main">
        <ChatWindow
          :messages="chatStore.messages"
          :is-loading="chatStore.isLoadingMessages"
          :onSendFeedback="handleFeedback"
          :show-resources="lastShowResources" 
        />
        <ChatInput @send-message="handleSendMessage" />
        <div v-if="chatStore.sendMessageError" class="error-message">
          {{ chatStore.sendMessageError }}
        </div>
        <div v-if="feedbackError" class="error-message">
          {{ feedbackError }}
        </div>
        <div v-if="feedbackSuccess" class="success-message">
          Merci pour votre retour, il a bien été pris en compte !
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import ChatWindow from "@/components/Chat/ChatWindow.vue";
import ChatInput from "@/components/Chat/ChatInput.vue";
import { useChatStore } from "@/stores/chat";
import { useDataStore } from "@/stores/data";
import { useAuthStore } from "@/stores/auth";

const chatStore = useChatStore();
const dataStore = useDataStore();
const authStore = useAuthStore();

const feedbackError = ref(null);
const feedbackSuccess = ref(false);
const lastShowResources = ref(true);

const handleSendMessage = (payload) => {
  chatStore.sendMessage({
    message: payload.message,
    departement_id: payload.selectedDepartement,
    filiere_id: payload.selectedFiliere,
    show_resources: payload.showResources,
    user_id: payload.selectedUser,
    profile_id: payload.selectedProfile
  });
  feedbackError.value = null;
  feedbackSuccess.value = false;
};

async function handleFeedback(feedbackText) {
  feedbackError.value = null;
  feedbackSuccess.value = false;
  const result = await chatStore.sendFeedback(feedbackText);
  if (result) {
    feedbackSuccess.value = true;
  } else {
    feedbackError.value = "Erreur lors de l'envoi du feedback. Veuillez réessayer.";
  }
}
</script>

<style scoped>
.chat-view-container {
  padding: 10px;
  max-width: 1400px;
  overflow: hidden;
  margin: 0 auto;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
  color: #333;
}
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chat-layout {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.error-message {
  color: #d32f2f;
  margin-top: 10px;
  background: #ffeaea;
  border-radius: 4px;
  padding: 6px 10px;
  font-size: 1em;
}
.success-message {
  color: #2ecc40;
  margin-top: 10px;
  background: #eaffea;
  border-radius: 4px;
  padding: 6px 10px;
  font-size: 1em;
}
</style>