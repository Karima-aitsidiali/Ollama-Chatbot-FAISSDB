<template>
  <div class="chat-window" ref="chatWindowRef">
    <MessageItem
      v-for="msg in messages"
      :key="msg.id"
      :message="msg"
      :show-resources="show_resources"
    />
    <!-- FeedbackForm juste après la dernière réponse du bot -->
    <FeedbackForm v-if="showFeedbackForm" :onSend="onSendFeedback" />
    <div v-if="isLoading" class="loading-indicator">
      <div class="typing-animation" aria-label="Le bot écrit">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
      <p>Le bot est en train d’écrire…</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, computed } from "vue";
import MessageItem from "./MessageItem.vue";
import FeedbackForm from "./FeedbackForm.vue";
import { useChatStore } from "@/stores/chat";

const props = defineProps({
  messages: {
    type: Array,
    required: true,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  onSendFeedback: {
    type: Function,
    required: true,
  },
  show_resources: {
    // <-- AJOUTE CETTE PROP
    type: Boolean,
    default: true, // Toujours afficher les ressources quand elles existent
  },
});

const chatStore = useChatStore();
const chatWindowRef = ref(null);

// Trouver le dernier message du bot
const lastBotMessage = computed(() => {
  return [...props.messages].reverse().find((m) => m.sender === "bot");
});

// Afficher le feedback seulement si c'est la dernière réponse du bot, et pas déjà envoyé
const showFeedbackForm = computed(
  () =>
    lastBotMessage.value &&
    lastBotMessage.value.chat_id === chatStore.lastChatId &&
    !chatStore.feedbackSentForLastResponse
);

// Scroll automatique désactivé si FeedbackForm affiché
watch(
  () => props.messages,
  async () => {
    await nextTick();
    if (chatWindowRef.value && !showFeedbackForm.value) {
      chatWindowRef.value.scrollTop = chatWindowRef.value.scrollHeight;
    }
  },
  { deep: true }
);
</script>

<style scoped>
.chat-window {
  flex-grow: 1;
  border: 2px solid #b3d8fd;
  padding: 24px 20px 18px 20px;
  width: 100%;
  height: 440px;
  background: linear-gradient(120deg, #f8fafc 80%, #eaf2fb 100%);
  border-radius: 18px;
  margin-bottom: 18px;
  box-shadow: 0 8px 32px rgba(52,152,219,0.13), 0 1.5px 0 #b3d8fd inset;
  scroll-behavior: smooth;
  transition: box-shadow 0.2s, border-color 0.2s;
  overflow-y: auto;
}

.chat-window:hover {
  box-shadow: 0 16px 48px rgba(52,152,219,0.18), 0 1.5px 0 #217dbb inset;
  border-color: #217dbb;
}

@media (max-width: 800px) {
  .chat-window {
    padding: 10px 4px 8px 4px;
    height: 320px;
    border-radius: 10px;
  }
}
.loading-indicator {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 20px;
  background-color: #eaf2fb;
  border-radius: 18px;
  width: fit-content;
  margin: 12px 0;
  box-shadow: 0 1px 4px rgba(52, 152, 219, 0.08);
}
.typing-animation {
  display: flex;
  align-items: center;
  height: 24px;
}
.typing-dot {
  width: 10px;
  height: 10px;
  background-color: #217dbb;
  border-radius: 50%;
  margin: 0 3px;
  animation: typingAnimation 1.4s infinite ease-in-out;
}
.typing-dot:nth-child(1) {
  animation-delay: 0s;
}
.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}
.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes typingAnimation {
  0%,
  60%,
  100% {
    transform: translateY(0);
    opacity: 0.6;
  }
  30% {
    transform: translateY(-7px);
    opacity: 1;
  }
}
.loading-indicator p {
  margin: 0;
  color: #217dbb;
  font-size: 1em;
  font-style: italic;
  font-weight: 500;
  letter-spacing: 0.2px;
}
@media (max-width: 800px) {
  .chat-window {
    padding: 10px 4px 8px 4px;
    height: 320px;
    border-radius: 10px;
  }
  .loading-indicator {
    padding: 8px 10px;
    font-size: 0.95em;
  }
}
</style>