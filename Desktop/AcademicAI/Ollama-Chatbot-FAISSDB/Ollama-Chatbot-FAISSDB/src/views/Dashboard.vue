<!-- src/views/Dashboard.vue -->
<template>
  <div class="dashboard-page">
    <div class="dashboard-container">
      <header class="dashboard-header">
        <h1>📊 Dashboard d'Analyse des Sentiments</h1>
        <p>Visualisation des retours utilisateurs sur le contenu pédagogique.</p>
      </header>
      
      <main class="dashboard-content">
        <!-- On importe et on affiche notre composant ici -->
        <DashSentiment />
      </main>
    </div>
  </div>
</template>

<script setup>
// J'ai vu que vous aviez mis DashSentiment dans un sous-dossier, c'est une bonne pratique !
// Assurez-vous que ce chemin est correct.
import DashSentiment from '@/components/AnalyseSentiment/DashSentiment.vue';
</script>

<style scoped>
.dashboard-page {
  /* Un fond subtil pour toute la page */
  background-color: #f8f9fa;
  padding: 2rem 1rem; /* Plus de padding sur mobile */
  min-height: calc(100vh - 100px); /* Prend toute la hauteur moins la navbar approx. */
}

.dashboard-container {
  max-width: 1600px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #dee2e6;
}

.dashboard-header h1 {
  font-size: 2.2rem;
  color: #212529;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.dashboard-header p {
  font-size: 1.1rem;
  color: #6c757d;
  margin: 0;
}

.dashboard-content {
  /* Le contenu principal où le dashboard sera affiché */
  background-color: transparent; /* Le fond est géré par la page */
}

@media (min-width: 768px) {
  .dashboard-page {
    padding: 2.5rem;
  }
  .dashboard-header h1 {
    font-size: 2.5rem;
  }
}
</style>