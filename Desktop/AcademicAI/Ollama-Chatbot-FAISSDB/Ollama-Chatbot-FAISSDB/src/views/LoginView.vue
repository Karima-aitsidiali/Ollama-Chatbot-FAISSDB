<template>
  <div class="login-view">
    <LoginForm v-if="!authStore.changePasswordRequired" />
    <ChangePasswordForm v-else />
    
    <!-- Mode invité button overlay -->
    <div v-if="!authStore.changePasswordRequired" class="guest-mode-overlay">
      <button @click="activateInviteMode()" class="guest-btn">
        <i class="guest-icon"></i>
        Mode Invité
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import LoginForm from '@/components/Auth/LoginForm.vue';
import ChangePasswordForm from '@/components/Auth/ChangePasswordForm.vue';
import { useAuthStore } from '@/stores/auth';

import router from '@/router';

const authStore = useAuthStore();

function disableInviteMode() {
  authStore.setInviteMode(false);
}

const activateInviteMode = async () => {
  console.log("Activation mode invité");
  await authStore.login({ username: "Invité", password: "1" });
  // Redirection ou autres actions...
}
</script>

<style scoped>
.login-view {
  position: relative;
  width: 100%;
  height: 100vh;
}

.guest-mode-overlay {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
}

.guest-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.95);
  color: #75a4c4;
  border: 2px solid rgba(117, 164, 196, 0.3);
  border-radius: 50px;
  font-size: 0.95em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 25px rgba(117, 164, 196, 0.15);
}

.guest-btn:hover {
  background: rgba(117, 164, 196, 0.1);
  border-color: #75a4c4;
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(117, 164, 196, 0.25);
}

.guest-icon {
  width: 16px;
  height: 16px;
  background: linear-gradient(45deg, #75a4c4, #217dbb);
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 7C14.6 7 14.2 7.1 13.9 7.4L13 8.3C12.4 8.9 11.6 8.9 11 8.3L10.1 7.4C9.8 7.1 9.4 7 9 7L3 7V9C3 9.6 3.4 10 4 10L9 10V16C9 16.6 9.4 17 10 17H14C14.6 17 15 16.6 15 16V10L20 10C20.6 10 21 9.6 21 9Z'/%3E%3C/svg%3E") no-repeat center;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 7C14.6 7 14.2 7.1 13.9 7.4L13 8.3C12.4 8.9 11.6 8.9 11 8.3L10.1 7.4C9.8 7.1 9.4 7 9 7L3 7V9C3 9.6 3.4 10 4 10L9 10V16C9 16.6 9.4 17 10 17H14C14.6 17 15 16.6 15 16V10L20 10C20.6 10 21 9.6 21 9Z'/%3E%3C/svg%3E") no-repeat center;
}

@media (max-width: 480px) {
  .guest-mode-overlay {
    bottom: 20px;
  }
  
  .guest-btn {
    padding: 10px 20px;
    font-size: 0.9em;
  }
}
</style>