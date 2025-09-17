<template>
  <transition name="fade-slide">
    <div class="feedback-form" v-if="!sent">
      <span>Exprime ton ressenti sur cette réponse :</span>
      <textarea
        v-model="feedbackText"
        :disabled="isSending"
        placeholder="Écris ici ton avis, ton ressenti, une suggestion…"
        rows="2"
        class="feedback-textarea"
      ></textarea>
      <button @click="send" :disabled="isSending || !feedbackText">
        Envoyer
      </button>
    </div>
  </transition>
  <transition name="fade-slide">
    <div v-if="sent" class="success-msg">
      Merci pour ton retour !
    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  onSend: Function,
});

const feedbackText = ref('');
const isSending = ref(false);
const sent = ref(false);

async function send() {
  if (!feedbackText.value.trim() || isSending.value) return;
  isSending.value = true;
  try {
    await props.onSend(feedbackText.value.trim());
    sent.value = true;
  } finally {
    isSending.value = false;
  }
}
</script>

<style scoped>
.feedback-form {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 400px;
  background: #f4faff;
  border-radius: 8px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(52,152,219,0.07);
  border: 1px solid #b3d8fd;
  animation: fadeInUp 0.5s;
}
.feedback-textarea {
  width: 100%;
  border-radius: 6px;
  border: 1px solid #b3d8fd;
  padding: 6px;
  font-size: 1em;
  resize: vertical;
}
.success-msg {
  color: #2ecc40;
  margin-top: 12px;
  background: #eaffea;
  border-radius: 6px;
  padding: 10px 16px;
  font-size: 1em;
  text-align: left;
  animation: fadeInUp 0.5s;
}
button {
  align-self: flex-end;
  border: none;
  background: #217dbb;
  color: white;
  border-radius: 6px;
  padding: 6px 16px;
  cursor: pointer;
  font-size: 1em;
  transition: background 0.2s;
}
button:hover:not(:disabled) {
  background: #145a8a;
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Animation */
.fade-slide-enter-active, .fade-slide-leave-active {
  transition: all 0.5s cubic-bezier(.55,0,.1,1);
}
.fade-slide-enter-from, .fade-slide-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
.fade-slide-enter-to, .fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>