<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <div class="logo-wrapper">
          <img src="@/assets/logo.png" alt="AcademicAI Logo" class="register-logo" />
        </div>
        <h2>Créer un compte AcademicAI</h2>
        <p class="register-subtitle">Rejoignez la communauté éducative</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="username">
            <i class="icon user-icon"></i>
            Nom d'utilisateur
          </label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required 
            autocomplete="username"
            placeholder="Choisissez un nom d'utilisateur" 
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
            autocomplete="new-password"
            placeholder="Créez un mot de passe sécurisé"
          />
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">
            <i class="icon check-icon"></i>
            Confirmer le mot de passe
          </label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            required 
            autocomplete="new-password"
            placeholder="Répétez votre mot de passe"
          />
        </div>
        
        <div class="form-group">
          <label for="profile">
            <i class="icon profile-icon"></i>
            Profil
          </label>
          <select 
            id="profile" 
            v-model="profileId" 
            required
            class="form-select"
          >
            <option value="" disabled>Sélectionnez votre profil</option>
            <option value="2">Professeur</option>
            <option value="3">Étudiant</option>
          </select>
        </div>
        
        <div v-if="errorMessage" class="message error-message">
          <i class="message-icon error-icon"></i>
          {{ errorMessage }}
        </div>
        
        <div v-if="successMessage" class="message success-message">
          <i class="message-icon success-icon"></i>
          {{ successMessage }}
        </div>
        
        <button 
          type="submit" 
          :disabled="isLoading" 
          class="register-btn"
        >
          <span v-if="!isLoading">Créer mon compte</span>
          <span v-else class="loading-text">
            <i class="loading-spinner"></i>
            Création en cours...
          </span>
        </button>
      </form>
      
      <div class="register-footer">
        <router-link to="/login" class="login-link">
          Déjà un compte ? Se connecter
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const confirmPassword = ref("");
const profileId = ref("");
const errorMessage = ref("");
const successMessage = ref("");
const isLoading = ref(false);

const authStore = useAuthStore();
const router = useRouter();

const handleRegister = async () => {
  errorMessage.value = "";
  successMessage.value = "";
  
  if (!username.value.trim()) {
    errorMessage.value = "Le nom d'utilisateur est obligatoire.";
    return;
  }
  
  if (password.value.length < 6) {
    errorMessage.value = "Le mot de passe doit contenir au moins 6 caractères.";
    return;
  }
  
  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Les mots de passe ne correspondent pas.";
    return;
  }
  
  if (!profileId.value) {
    errorMessage.value = "Veuillez sélectionner un profil.";
    return;
  }
  
  try {
    isLoading.value = true;
    
    await authStore.register({
      username: username.value,
      password: password.value,
      profile_id: parseInt(profileId.value)
    });
    
    if (authStore.registerError) {
      errorMessage.value = authStore.registerError;
    } else {
      successMessage.value = "Compte créé avec succès ! Redirection...";
      setTimeout(() => {
        router.push("/login");
      }, 2000);
    }
  } catch (error) {
    errorMessage.value = "Une erreur est survenue lors de la création du compte.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #74a3c3 0%, #75a4c4 50%, #76a5c5 100%);
  padding: 20px;
}

.register-card {
  max-width: 450px;
  width: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(33, 125, 187, 0.15);
  padding: 40px 35px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-family: 'Segoe UI', Arial, sans-serif;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo-wrapper {
  margin-bottom: 15px;
}

.register-logo {
  height: 70px;
  width: auto;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(33, 125, 187, 0.1);
}

h2 {
  margin: 0 0 8px 0;
  color: #217dbb;
  font-size: 1.7em;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.register-subtitle {
  color: #5a6c7d;
  font-size: 0.95em;
  margin: 0;
  font-style: italic;
  font-weight: 500;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 22px;
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
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z'/%3E%3C/svg%3E") no-repeat center;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z'/%3E%3C/svg%3E") no-repeat center;
}

.lock-icon {
  background: linear-gradient(45deg, #f1c40f, #f39c12);
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M18 8H17V6C17 3.24 14.76 1 12 1S7 3.24 7 6V8H6C4.9 8 4 8.9 4 10V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V10C20 8.9 19.1 8 18 8ZM9 6C9 4.34 10.34 3 12 3S15 4.34 15 6V8H9V6Z'/%3E%3C/svg%3E") no-repeat center;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M18 8H17V6C17 3.24 14.76 1 12 1S7 3.24 7 6V8H6C4.9 8 4 8.9 4 10V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V10C20 8.9 19.1 8 18 8ZM9 6C9 4.34 10.34 3 12 3S15 4.34 15 6V8H9V6Z'/%3E%3C/svg%3E") no-repeat center;
}

.check-icon {
  background: linear-gradient(45deg, #27ae60, #2ecc71);
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E") no-repeat center;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E") no-repeat center;
}

.profile-icon {
  background: linear-gradient(45deg, #9b59b6, #8e44ad);
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z'/%3E%3C/svg%3E") no-repeat center;
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z'/%3E%3C/svg%3E") no-repeat center;
}

.form-group input,
.form-select {
  padding: 14px 16px;
  border: 2px solid #e3ecf0;
  border-radius: 10px;
  font-size: 1em;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
  color: #34495e;
  font-weight: 500;
}

.form-group input:focus,
.form-select:focus {
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

.form-select option {
  padding: 12px;
  background: #fff;
  color: #34495e;
}

.register-btn {
  padding: 16px 0;
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1em;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(39, 174, 96, 0.2);
  margin-top: 10px;
  letter-spacing: 0.5px;
  position: relative;
  overflow: hidden;
}

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(39, 174, 96, 0.3);
}

.register-btn:disabled {
  background: linear-gradient(135deg, #a8e6cf, #c8e6c9);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 4px 15px rgba(39, 174, 96, 0.1);
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
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z'/%3E%3C/svg%3E") no-repeat center;
}

.success-icon {
  background: #155724;
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'/%3E%3C/svg%3E") no-repeat center;
}

.register-footer {
  text-align: center;
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid rgba(116, 163, 195, 0.2);
}

.login-link {
  color: #75a4c4;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95em;
  transition: all 0.3s ease;
  padding: 8px 12px;
  border-radius: 6px;
}

.login-link:hover {
  color: #217dbb;
  background: rgba(117, 164, 196, 0.1);
  text-decoration: none;
}

@media (max-width: 480px) {
  .register-container {
    padding: 15px;
  }
  
  .register-card {
    padding: 30px 25px;
  }
  
  h2 {
    font-size: 1.5em;
  }
  
  .register-form {
    gap: 18px;
  }
  
  .form-group input,
  .form-select {
    padding: 12px 14px;
  }
  
  .register-btn {
    padding: 14px 0;
    font-size: 1em;
  }
}
</style>