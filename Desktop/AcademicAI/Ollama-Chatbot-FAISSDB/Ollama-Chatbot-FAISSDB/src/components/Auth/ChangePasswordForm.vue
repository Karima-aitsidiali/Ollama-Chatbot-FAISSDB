<template>
  <div class="change-password-container">
    <div class="change-password-card">
      <div class="change-password-header">
        <div class="icon-wrapper">
          <i class="main-icon key-icon"></i>
        </div>
        <h2>Changer le mot de passe</h2>
        <p class="change-password-subtitle">Sécurisez votre accès à AcademicAI</p>
      </div>
      
      <form @submit.prevent="handleChangePassword" class="change-password-form">
        <div class="form-group">
          <label for="old-password">
            <i class="icon lock-icon"></i>
            Ancien mot de passe
          </label>
          <input 
            type="password" 
            id="old-password" 
            v-model="oldPassword" 
            required 
            placeholder="Saisissez votre mot de passe actuel"
          />
        </div>
        
        <div class="form-group">
          <label for="new-password">
            <i class="icon new-icon"></i>
            Nouveau mot de passe
          </label>
          <input 
            type="password" 
            id="new-password" 
            v-model="newPassword" 
            required 
            placeholder="Créez un nouveau mot de passe"
          />
        </div>
        
        <div class="form-group">
          <label for="confirm-password">
            <i class="icon check-icon"></i>
            Confirmer le nouveau mot de passe
          </label>
          <input
            type="password"
            id="confirm-password"
            v-model="confirmPassword"
            required
            placeholder="Répétez le nouveau mot de passe"
          />
        </div>
        
        <div v-if="errorMessage" class="message error-message">
          <i class="message-icon error-icon"></i>
          {{ errorMessage }}
        </div>
        
        <div v-if="authStore.changePasswordError" class="message error-message">
          <i class="message-icon error-icon"></i>
          {{ authStore.changePasswordError }}
        </div>
        
        <div v-if="authStore.changePasswordSuccess" class="message success-message">
          <i class="message-icon success-icon"></i>
          {{ authStore.changePasswordSuccess }}
        </div>
        
        <button 
          type="submit" 
          :disabled="authStore.isLoading"
          class="change-password-btn"
        >
          <span v-if="!authStore.isLoading">Changer le mot de passe</span>
          <span v-else class="loading-text">
            <i class="loading-spinner"></i>
            Modification en cours...
          </span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const oldPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const errorMessage = ref(null);
const authStore = useAuthStore();

const handleChangePassword = async () => {
  errorMessage.value = null;

  if (!oldPassword.value || !newPassword.value || !confirmPassword.value) {
    errorMessage.value = "Tous les champs sont obligatoires.";
    return;
  }

  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value =
      "Le nouveau mot de passe et sa confirmation ne correspondent pas.";
    return;
  }

  await authStore.changePassword(oldPassword.value, newPassword.value);

  if (authStore.changePasswordError) {
    errorMessage.value = authStore.changePasswordError;
  } else {
    errorMessage.value = null;
  }
};
</script>

<style scoped>
.change-password-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #74a3c3 0%, #75a4c4 50%, #76a5c5 100%);
  padding: 20px;
}

.change-password-card {
  max-width: 440px;
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(33, 125, 187, 0.15);
  padding: 40px 35px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-family: 'Segoe UI', Arial, sans-serif;
}

.change-password-header {
  text-align: center;
  margin-bottom: 32px;
}

.icon-wrapper {
  margin-bottom: 15px;
}

.main-icon {
  width: 50px;
  height: 50px;
  display: inline-block;
  border-radius: 50%;
}

.key-icon {
  background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%);
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M7 14c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm0-4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm12.78-1.38L15.44 12 14 10.56l4.34-4.34c.39-.39 1.02-.39 1.41 0l.03.03c.39.39.39 1.02 0 1.41z'/%3E%3C/svg%3E") no-repeat center;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M7 14c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm0-4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm12.78-1.38L15.44 12 14 10.56l4.34-4.34c.39-.39 1.02-.39 1.41 0l.03.03c.39.39.39 1.02 0 1.41z'/%3E%3C/svg%3E") no-repeat center;
}

h2 {
  margin: 0 0 8px 0;
  color: #217dbb;
  font-size: 1.7em;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.change-password-subtitle {
  color: #5a6c7d;
  font-size: 0.95em;
  margin: 0;
  font-style: italic;
  font-weight: 500;
}

.change-password-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  color: #34495e;
  font-weight: 600;
  font-size: 0.95em;
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon {
  width: 16px;
  height: 16px;
  display: inline-block;
  border-radius: 3px;
}

.lock-icon {
  background: linear-gradient(45deg, #e74c3c, #c0392b);
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M18 8H17V6C17 3.24 14.76 1 12 1S7 3.24 7 6V8H6C4.9 8 4 8.9 4 10V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V10C20 8.9 19.1 8 18 8ZM9 6C9 4.34 10.34 3 12 3S15 4.34 15 6V8H9V6Z'/%3E%3C/svg%3E") no-repeat center;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M18 8H17V6C17 3.24 14.76 1 12 1S7 3.24 7 6V8H6C4.9 8 4 8.9 4 10V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V10C20 8.9 19.1 8 18 8ZM9 6C9 4.34 10.34 3 12 3S15 4.34 15 6V8H9V6Z'/%3E%3C/svg%3E") no-repeat center;
}

.new-icon {
  background: linear-gradient(45deg, #f1c40f, #f39c12);
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11H13v4h-2v-4H7v-2h4V7h2v4h4v2z'/%3E%3C/svg%3E") no-repeat center;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11H13v4h-2v-4H7v-2h4V7h2v4h4v2z'/%3E%3C/svg%3E") no-repeat center;
}

.check-icon {
  background: linear-gradient(45deg, #27ae60, #2ecc71);
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E") no-repeat center;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E") no-repeat center;
}

.form-group input {
  padding: 14px 16px;
  border: 2px solid #e3ecf0;
  border-radius: 10px;
  font-size: 1em;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
  color: #34495e;
  font-weight: 500;
}

.form-group input:focus {
  border-color: #75a4c4;
  outline: none;
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 0 0 3px rgba(117, 164, 196, 0.1);
  transform: translateY(-1px);
}

.form-group input::placeholder {
  color: #95a5a6;
  font-weight: 400;
}

.change-password-btn {
  padding: 16px 0;
  background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%);
  color: #2c3e50;
  border: none;
  border-radius: 12px;
  font-size: 1.1em;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(241, 196, 15, 0.2);
  margin-top: 10px;
  letter-spacing: 0.5px;
  position: relative;
  overflow: hidden;
}

.change-password-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(241, 196, 15, 0.3);
}

.change-password-btn:disabled {
  background: linear-gradient(135deg, #fdeaa7, #f9e79f);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 4px 15px rgba(241, 196, 15, 0.1);
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(44, 62, 80, 0.3);
  border-top: 2px solid #2c3e50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 0.95em;
  font-weight: 500;
  margin: -5px 0;
}

.error-message {
  color: #c0392b;
  background: linear-gradient(135deg, #fdecea, #f8d7da);
  border: 1px solid #f5c6cb;
}

.success-message {
  color: #155724;
  background: linear-gradient(135deg, #d1edcc, #c3e6cb);
  border: 1px solid #c3e6cb;
}

.message-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.error-icon {
  background: #c0392b;
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z'/%3E%3C/svg%3E") no-repeat center;
}

.success-icon {
  background: #155724;
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'/%3E%3C/svg%3E") no-repeat center;
}

@media (max-width: 480px) {
  .change-password-container {
    padding: 15px;
  }
  
  .change-password-card {
    padding: 30px 25px;
  }
  
  h2 {
    font-size: 1.5em;
  }
  
  .change-password-form {
    gap: 20px;
  }
  
  .form-group input {
    padding: 12px 14px;
  }
  
  .change-password-btn {
    padding: 14px 0;
    font-size: 1em;
  }
  
  .main-icon {
    width: 40px;
    height: 40px;
  }
}
</style>