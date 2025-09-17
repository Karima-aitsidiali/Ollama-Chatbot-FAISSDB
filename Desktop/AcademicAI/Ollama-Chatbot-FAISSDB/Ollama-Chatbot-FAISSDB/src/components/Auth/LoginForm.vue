<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo-wrapper">
          <img src="@/assets/logo.png" alt="AcademicAI Logo" class="login-logo" />
        </div>
        <h2>Connexion à AcademicAI</h2>
        <p class="login-subtitle">L'IA au service de l'éducation</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">
            <i class="icon user-icon"></i>
            Identifiant
          </label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required 
            autocomplete="username"
            placeholder="Votre nom d'utilisateur" 
          />
        </div>
        
        <div class="form-group">
          <label for="password">
            <i class="icon lock-icon"></i>
            Mot de passe
          </label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            autocomplete="current-password"
            placeholder="Votre mot de passe"
          />
        </div>
        
        <div v-if="authStore.loginError" class="message error-message">
          <i class="message-icon error-icon"></i>
          {{ authStore.loginError }}
        </div>
        
        <div v-if="authStore.loginSuccess" class="message success-message">
          <i class="message-icon success-icon"></i>
          {{ authStore.loginSuccess }}
        </div>
        
        <button 
          type="submit" 
          :disabled="authStore.isLoading" 
          @click="disableInviteMode"
          class="login-btn"
        >
          <span v-if="!authStore.isLoading">Se connecter</span>
          <span v-else class="loading-text">
            <i class="loading-spinner"></i>
            Connexion en cours...
          </span>
        </button>
      </form>
      
      <div class="login-footer">
        <router-link to="/register" class="register-link">
          Créer un compte
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const username = ref("");
const password = ref("");
const authStore = useAuthStore();

function disableInviteMode() {
  authStore.setInviteMode(false);
}

const handleLogin = async () => {
  await authStore.login({ username: username.value, password: password.value });
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: red !important;
  padding: 20px;
}

.login-card {
  max-width: 420px;
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(33, 125, 187, 0.15);
  padding: 40px 35px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-family: 'Segoe UI', Arial, sans-serif;
}

.login-header {
  text-align: center;
  margin-bottom: 35px;
}

.logo-wrapper {
  margin-bottom: 15px;
}

.login-logo {
  height: 70px;
  width: auto;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(33, 125, 187, 0.1);
}

h2 {
  margin: 0 0 8px 0;
  color: #217dbb;
  font-size: 1.8em;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.login-subtitle {
  color: #5a6c7d;
  font-size: 0.95em;
  margin: 0;
  font-style: italic;
  font-weight: 500;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 25px;
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

.user-icon {
  background: linear-gradient(45deg, #f1c40f, #f39c12);
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 7C14.6 7 14.2 7.1 13.9 7.4L13 8.3C12.4 8.9 11.6 8.9 11 8.3L10.1 7.4C9.8 7.1 9.4 7 9 7L3 7V9C3 9.6 3.4 10 4 10L9 10V16C9 16.6 9.4 17 10 17H14C14.6 17 15 16.6 15 16V10L20 10C20.6 10 21 9.6 21 9Z'/%3E%3C/svg%3E") no-repeat center;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 7C14.6 7 14.2 7.1 13.9 7.4L13 8.3C12.4 8.9 11.6 8.9 11 8.3L10.1 7.4C9.8 7.1 9.4 7 9 7L3 7V9C3 9.6 3.4 10 4 10L9 10V16C9 16.6 9.4 17 10 17H14C14.6 17 15 16.6 15 16V10L20 10C20.6 10 21 9.6 21 9Z'/%3E%3C/svg%3E") no-repeat center;
}

.lock-icon {
  background: linear-gradient(45deg, #f1c40f, #f39c12);
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M18 8H17V6C17 3.24 14.76 1 12 1S7 3.24 7 6V8H6C4.9 8 4 8.9 4 10V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V10C20 8.9 19.1 8 18 8ZM9 6C9 4.34 10.34 3 12 3S15 4.34 15 6V8H9V6Z'/%3E%3C/svg%3E") no-repeat center;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M18 8H17V6C17 3.24 14.76 1 12 1S7 3.24 7 6V8H6C4.9 8 4 8.9 4 10V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V10C20 8.9 19.1 8 18 8ZM9 6C9 4.34 10.34 3 12 3S15 4.34 15 6V8H9V6Z'/%3E%3C/svg%3E") no-repeat center;
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

.login-btn {
  padding: 16px 0;
  background: linear-gradient(135deg, #75a4c4 0%, #217dbb 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1em;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(33, 125, 187, 0.2);
  margin-top: 10px;
  letter-spacing: 0.5px;
  position: relative;
  overflow: hidden;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(33, 125, 187, 0.3);
}

.login-btn:disabled {
  background: linear-gradient(135deg, #b2dffc, #d6eaff);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 4px 15px rgba(33, 125, 187, 0.1);
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
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
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
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'/%3E%3C/svg%3E") no-repeat center;
}

.success-icon {
  background: #155724;
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'/%3E%3C/svg%3E") no-repeat center;
}

.login-footer {
  text-align: center;
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid rgba(116, 163, 195, 0.2);
}

.register-link {
  color: #75a4c4;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95em;
  transition: all 0.3s ease;
  padding: 8px 12px;
  border-radius: 6px;
}

.register-link:hover {
  color: #217dbb;
  background: rgba(117, 164, 196, 0.1);
  text-decoration: none;
}

@media (max-width: 480px) {
  .login-container {
    padding: 15px;
  }
  
  .login-card {
    padding: 30px 25px;
  }
  
  h2 {
    font-size: 1.6em;
  }
  
  .form-group input {
    padding: 12px 14px;
  }
  
  .login-btn {
    padding: 14px 0;
    font-size: 1em;
  }
}
</style>