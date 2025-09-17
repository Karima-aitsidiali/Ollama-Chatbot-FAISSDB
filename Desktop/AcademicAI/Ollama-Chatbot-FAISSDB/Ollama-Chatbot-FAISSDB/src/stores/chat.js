// stores/chat.js
import { defineStore } from 'pinia';
import api from '@/services/api'; // Assurez-vous que le chemin est correct
import { useAuthStore } from '@/stores/auth'; // Assurez-vous que le chemin est correct

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [], // Pour les messages de la session de chat active
    chatHistory: [], // Pour l'historique des conversations
    isLoadingMessages: false, // Pour l'envoi de messages
    isLoadingHistory: false, // Pour le chargement de l'historique
    sendMessageError: null,
    fetchHistoryError: null, // Pour les erreurs de chargement de l'historique

    // NOUVEAU: Pour gérer le feedback de la dernière réponse
    lastChatId: null, // ID de la dernière réponse du bot
    feedbackSentForLastResponse: false, // Indicateur si le feedback a été envoyé pour cette réponse
  }),
  actions: {
    /**
     * Ajoute un message à l'historique des messages actifs.
     * @param {object} message - L'objet message à ajouter.
     */
    addMessage(message) {
      // Ajoute un ID et un timestamp si non présents
      this.messages.push({
        ...message,
        id: message.id || Date.now() + Math.random(), // Utilisez l'ID du message s'il existe (ex: pour l'historique)
        timestamp: message.timestamp || new Date(),
        resources: message.resources || [], // <-- ESSENTIEL !
      });
      console.log(this.messages[this.messages.length - 1]);
    },

    /**
     * Envoie un message au chatbot et gère la réponse.
     * @param {object} payload - Les données du message et des filtres (message, departement_id, etc.).
     */
    async sendMessage(payload) {
      const authStore = useAuthStore();

      // Vérification de l'authentification et des IDs requis
      if (!authStore.isAuthenticated || !authStore.userId || !authStore.profileId) {
        this.sendMessageError = "Utilisateur non authentifié ou IDs manquants pour l'envoi du message.";
        console.error("sendMessage: User not authenticated or missing IDs.");
        return;
      }

      // Ajoute le message de l'utilisateur immédiatement à l'affichage
      this.addMessage({ text: payload.message, sender: 'user' });
      this.isLoadingMessages = true;
      this.sendMessageError = null;
      this.feedbackSentForLastResponse = false; // Réinitialiser le feedback pour la nouvelle conversation

      const chatRequestData = {
        message: payload.message,
        departement_id: parseInt(payload.departement_id) || null,
        filiere_id: parseInt(payload.filiere_id) || null,
        module_id: parseInt(payload.module_id) || null,
        activite_id: parseInt(payload.activite_id) || null,
        profile_id: parseInt(payload.profile_id) || null,
        show_resources: payload.show_resources === true, // force booléen
        user_id: parseInt(payload.user_id) || null, // Assurez-vous que c'est bien l'ID de l'utilisateur authentifié
      };

      try {
        const response = await api.sendMessage(chatRequestData);
        // Vérification de la réponse du backend
        console.log("Réponse brute du backend :", response.data);

        // Extraction des données de la réponse du backend, y compris chat_id
        const { response: botResponseText, chat_id: receivedChatId, resources: botResources } = response.data;

        // Ajoute la réponse du bot à l'affichage
        this.addMessage({
          text: botResponseText,
          sender: 'bot',
          chat_id: receivedChatId, // Stocke l'ID avec le message dans le tableau messages
          resources: botResources || [] // S'assure que les ressources sont un tableau
        });

        // Met à jour l'ID de la dernière conversation pour le feedback
        this.lastChatId = receivedChatId;
        console.log("lastChatId mis à jour :", this.lastChatId);

      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || "Erreur lors de l'envoi du message.";
        this.sendMessageError = errorMessage;
        this.addMessage({ text: `Erreur: ${errorMessage}`, sender: 'bot', isError: true });
        console.error("Erreur sendMessage:", error);
      } finally {
        this.isLoadingMessages = false;
      }
    },

    /**
     * Récupère l'historique des conversations de l'utilisateur.
     * @param {object} filters - Filtres optionnels pour la récupération de l'historique.
     */
    async fetchChatHistory(filters = {}) {
      const authStore = useAuthStore();

      if (!authStore.isAuthenticated || !authStore.userId || !authStore.profileId) {
        this.fetchHistoryError = "Utilisateur non authentifié ou IDs manquants pour récupérer l'historique.";
        this.chatHistory = [];
        return;
      }

      this.isLoadingHistory = true;
      this.fetchHistoryError = null;
      try {
        const params = {
          profile_id: authStore.profileId,
          user_id: authStore.userId,
          ...filters,
        };
        const response = await api.getChatHistory(params);
        this.chatHistory = response.data || [];
      } catch (error) {
        this.fetchHistoryError = "Impossible de charger l'historique des conversations.";
        console.error("Erreur fetchChatHistory:", error);
        this.chatHistory = [];
      } finally {
        this.isLoadingHistory = false;
      }
    },

    async sendFeedback(feedbackText) {
      const authStore = useAuthStore();
      const user_id = authStore.userId;

      if (!this.lastChatId) {
        console.warn("Impossible d'envoyer le feedback : aucun chat_id disponible.");
        return false;
      }
      if (this.feedbackSentForLastResponse) {
        console.log("Feedback déjà envoyé pour cette réponse.");
        return false;
      }

      try {
        await api.sendFeedback({
          chat_message_id: this.lastChatId,
          sentiment: feedbackText,
          user_id: user_id
        });
        this.feedbackSentForLastResponse = true;
        console.log('Feedback texte envoyé avec succès pour chat_id:', this.lastChatId);
        return true;
      } catch (error) {
        console.error("Erreur lors de l'envoi du feedback:", error);
        return false;
      }
    },
    /**
     * Réinitialise l'état de la session de chat active.
     */
    clearChat() {
      this.messages = [];
      this.lastChatId = null; // Réinitialise l'ID du chat et l'état du feedback
      this.feedbackSentForLastResponse = false;
      this.isLoadingMessages = false;
      this.sendMessageError = null;
      this.isLoadingHistory = false;
      this.fetchHistoryError = null;
      this.chatHistory = [];
      console.log("Session de chat réinitialisée.");
    }
  },
});