<!-- src/components/AnalyseSentiment/DashSentiment.vue -->
<template>
  <div class="sentiment-container">
    
    <!-- État de chargement (inchangé) -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Analyse des sentiments en cours...</p>
    </div>

    <!-- État d'erreur (inchangé) -->
    <div v-else-if="error" class="error-container">
      <h3>Oups ! Une erreur est survenue</h3>
      <p>{{ error }}</p>
      <button @click="runAnalysis" class="launch-button retry-button">
        <span class="icon">🔄</span> Réessayer
      </button>
    </div>

    <!-- État des résultats (SIMPLIFIÉ) -->
    <!-- Ce v-else-if est la seule condition nécessaire. Il affiche tout d'un coup. -->
    <div v-else-if="dashboardData" class="grid-container">
      
      <!-- Section KPIs -->
      <div class="kpi-card">
        <div class="kpi-header"><h3>📊 Feedbacks Totaux</h3></div>
        <p class="kpi-value">{{ dashboardData.kpis.total_feedbacks }}</p>
      </div>
      <div class="kpi-card">
        <div class="kpi-header"><h3>👥 Utilisateurs Uniques</h3></div>
        <p class="kpi-value">{{ dashboardData.kpis.unique_users }}</p>
      </div>
      <div class="kpi-card positive">
        <div class="kpi-header"><h3>👍 Taux de Positivité</h3></div>
        <p class="kpi-value">{{ dashboardData.kpis.positive_pct }}%</p>
      </div>

      <!-- Section Graphiques -->
      <div class="chart-card large-card">
        <h3>Distribution des Sentiments</h3>
        <!-- Le wrapper est la clé. Pas besoin de v-if supplémentaire ici. -->
        <div class="chart-wrapper">
          <PieChart 
            :chartData="dashboardData.charts.polarity_distribution"
            :chartOptions="pieChartOptions" 
          />
        </div>
      </div>
      <div class="chart-card large-card">
        <h3>% Positifs par Département-Filière</h3>
        <!-- Le wrapper est la clé. Pas besoin de v-if supplémentaire ici. -->
        <div class="chart-wrapper">
          <BarChart 
            :chartData="dashboardData.charts.positive_by_dept_filiere"
            :chartOptions="barChartOptions"
          />
        </div>
      </div>
      
      <!-- Section Tableaux -->
      <div class="table-card large-card">
        <h3>🏆 Top 8 Utilisateurs Actifs</h3>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Utilisateur</th>
                <th>Feedbacks</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in dashboardData.tables.top_users" :key="user.User">
                <td>{{ user.User }}</td>
                <td>{{ user.count }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- État initial (inchangé) -->
    <div v-else class="initial-state-container">
      <h2>Prêt à analyser les feedbacks ?</h2>
      <p>Cliquez sur le bouton pour lancer l'analyse et générer le tableau de bord.</p>
      <button @click="runAnalysis" class="launch-button">
        <span class="icon">🚀</span> Lancer l'analyse des sentiments
      </button>
    </div>

  </div>
</template>

<script setup>
// SIMPLIFIÉ : On retire nextTick
import { ref } from 'vue';
import api from '@/services/api';
import BarChart from '@/components/Charts/BarChart.vue';
import PieChart from '@/components/Charts/PieChart.vue';

const loading = ref(false);
const error = ref(null);
const dashboardData = ref(null);
// SIMPLIFIÉ : On retire la variable renderCharts
// const renderCharts = ref(false); // SUPPRIMÉ

// Les options des graphiques ne changent pas
const pieChartOptions = ref({ /* ... vos options ... */ });
const barChartOptions = ref({ /* ... vos options ... */ });

// SIMPLIFIÉ : La fonction runAnalysis n'a plus besoin de nextTick
async function runAnalysis() {
  loading.value = true;
  error.value = null;
  dashboardData.value = null;

  try {
    await new Promise(resolve => setTimeout(resolve, 500));
    const response = await api.getSentimentDashboard();
    dashboardData.value = response.data;
    // Il n'y a plus rien à faire ici. Le template va se mettre à jour
    // automatiquement et correctement.
  } catch (err) {
    error.value = "Impossible de charger les données. " + (err.response?.data?.detail || err.message);
    console.error(err);
  } finally {
    loading.value = false;
  }
}
</script>


<style scoped>
/* --- Conteneur principal --- */
.sentiment-container {
  width: 100%;
}

/* --- Animation de chargement --- */
.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  gap: 1rem;
}
.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 0, 0, 0.1);
  border-left-color: #74a3c3;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-container p { font-size: 1.2rem; color: #555; }

/* --- Conteneur d'erreur --- */
.error-container {
  background-color: #ffebee;
  color: #c62828;
  border: 1px solid #c62828;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
}
.error-container h3 { margin-top: 0; }

/* --- État initial et bouton de lancement --- */
.initial-state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 4rem 2rem;
  background-color: #f8f9fa;
  border-radius: 12px;
  min-height: 50vh;
}
.initial-state-container h2 { font-size: 1.8rem; color: #333; margin-bottom: 0.5rem; }
.initial-state-container p { font-size: 1.1rem; color: #666; max-width: 500px; margin-bottom: 2rem; }
.launch-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 24px;
  font-size: 1.1rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(90deg, #75a4c4 0%, #5a8eaf 100%);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}
.launch-button .icon { margin-right: 10px; font-size: 1.4rem; }
.launch-button:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15); }
.retry-button { margin-top: 1rem; background: #ffc107; color: #333; }

/* --- Grille et Cartes --- */
.grid-container {
  display: grid;
  /* AJUSTEMENT 2 : Largeur minimale des cartes augmentée */
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 1.5rem;
}
.kpi-card, .chart-card, .table-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.kpi-card:hover, .chart-card:hover, .table-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1); }

/* --- Cartes KPI --- */
.kpi-card { display: flex; flex-direction: column; }
.kpi-header h3 { font-size: 1.1rem; color: #333; margin: 0 0 0.5rem 0; }
.kpi-value { font-size: 2.8rem; font-weight: 700; color: #74a3c3; margin: auto 0 0 0; }
.kpi-card.positive .kpi-value { color: #2ecc71; }

/* --- Cartes Graphiques et Tableaux --- */
.chart-card, .table-card { grid-column: span 1; }
@media (min-width: 992px) {
  .large-card { grid-column: span 1; }
  .table-card { grid-column: span 1; }
}
.chart-card h3, .table-card h3 { margin-top: 0; margin-bottom: 1.5rem; color: #333; }

/* --- Wrapper pour les graphiques --- */
.chart-wrapper {
  position: relative;
  /* AJUSTEMENT 1 : Hauteur des graphiques réduite */
  height: 320px;
  width: 100%;
}

/* --- Style du Tableau --- */
.table-wrapper { width: 100%; overflow-x: auto; }
table { width: 100%; border-collapse: collapse; text-align: left; }
th, td { padding: 12px 15px; border-bottom: 1px solid #e0e0e0; }
thead tr { background-color: #f4f7f9; }
th { font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: #555; }
tbody tr:nth-child(even) { background-color: #f9fafb; }
tbody tr:hover { background-color: #f0f4f8; }
</style>