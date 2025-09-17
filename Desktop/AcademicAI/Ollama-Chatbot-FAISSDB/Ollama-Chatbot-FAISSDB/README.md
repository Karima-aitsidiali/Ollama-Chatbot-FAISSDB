<<<<<<< HEAD
# 🤖 AcademicAI Chatbot

Bienvenue dans **AcademicAI Chatbot** ! Ce chatbot Python fonctionne localement, s'appuie sur l'API Ollama Local (`http://localhost:11434/api/generate`) et le modèle multimodal **gemma3:4b** pour offrir une assistance académique rapide, fiable et hors-ligne.

---

## 🌟 Fonctionnalités

- **🏡 Exécution Locale**  
  Tout se passe sur votre machine : aucune connexion internet ou API externe requise, garantissant confidentialité et accès ininterrompu.

- **🤖 Chat IA**  
  Profitez de réponses intelligentes, contextuelles et adaptées à vos besoins éducatifs.

- **💻 Génération de Contenu**  
  Créez des cours complets, des quiz stimulants et des résumés concis de documents pédagogiques.

- **⚡ Léger et Rapide**  
  Utilise le modèle efficace **gemma3:4b** pour des performances optimales sans compromis sur la qualité.

- **🧠 RAG Avancé (Retrieval-Augmented Generation)**  
  - **Embedding** : Intégration avec `BAAI/bge-base-en-v1.5` pour des embeddings robustes et une compréhension sémantique précise.  
  - **Découpage & Recouvrement** : Découpe intelligente des documents en segments avec recouvrement pour préserver le contexte.  
  - **Base de Vecteurs** : Utilisation de **FaissDB** pour un stockage et une recherche rapide des informations pertinentes.  
  - **Similarité Cosinus** : Recherche des informations les plus proches sémantiquement.  
  - **Reranking** : Raffinement des résultats pour ne garder que les plus pertinents et cohérents.  
  - **Génération de Réponse** : Synthèse claire, concise et précise à partir des segments retrouvés.

- **🚀 Backend FastAPI**  
  Construit avec **FastAPI** pour une API robuste, performante et facile à utiliser.

---

## 📋 Prise en Main

Suivez ces étapes pour installer et lancer le chatbot :

### 1️⃣ Cloner le Dépôt

```bash
git clone https://github.com/ImasHF26/AcademicAI.git
cd AcademicAI
```

### 2️⃣ Installer les dépendances
Assurez-vous d’avoir Python 3.11 ou plus. Créez un environnement virtuel et installez les dépendances :

```bash
python -m venv .venv
.venv\Scripts\activate  # Sur Windows
pip install -r requirements.txt
```

### 3️⃣ Vérifier que l’API locale fonctionne 🖥️
Le chatbot s’appuie sur une API locale pour générer les réponses. Vérifiez que l’API Ollama fonctionne à l’adresse http://localhost:11434/api/generate.

Modèle utilisé : gemma3:4b  
Pourquoi ce modèle ? Il offre un bon compromis entre performance, rapidité et précision, idéal pour des conversations éducatives et la génération de contenu.

Si l’API n’est pas démarrée, référez-vous à la documentation officielle d’Ollama pour configurer le serveur local et télécharger le modèle gemma3:4b.

### 4️⃣ Lancer le chatbot 🚀
Une fois les dépendances installées et l’API locale démarrée, lancez le chatbot :

```bash
uvicorn api.main:app --reload
```

Ouvrez votre navigateur et rendez-vous à l’adresse indiquée par Uvicorn (généralement http://127.0.0.1:8000).

### 💬 Exemples d’utilisation
Commencez à discuter ! Par exemple, vous pouvez demander :

- "Qu'est ce qu'un perceptron ?"
- "Donne-moi une introduction au DevOps."
- "Crée un quiz sur l'apprentissage automatique."
- "Résume le concept de la régression linéaire."

---

## 📌 Tâches principales du projet

- Installation et configuration de l’environnement Python et des dépendances
- Mise en place et vérification de l’API Ollama et du modèle gemma3:4b
- Lancement du backend FastAPI
- Développement et maintenance des fonctionnalités principales (chat, génération de contenu, RAG, etc.)
- Tests et validation du fonctionnement du chatbot
- Documentation et amélioration continue

---

## 🤝 Contribution
Les contributions sont les bienvenues ! 🛠️

Si vous souhaitez contribuer, veuillez forker le dépôt, créer une branche pour vos fonctionnalités ou corrections, puis soumettre une pull request. Merci d'aider à améliorer AcademicAI !
=======
# AcademicAI FrontEnd

Ce projet est une interface web développée avec Vue 3 et Vite pour le chatbot éducatif AcademicAI.

## Prérequis
- Node.js (version recommandée : >=16)
- npm ou yarn

## Installation
1. Clonez le dépôt :
   ```bash
   git clone <url-du-repo>
   cd FrontEnd
   ```
2. Installez les dépendances :
   ```bash
   npm install
   # ou
   yarn install
   ```

## Lancement du projet en développement
```bash
npm run dev
# ou
yarn dev
```
Le projet sera accessible sur `http://localhost:5173` (par défaut).

## Tâches principales du projet
- **Développement de l'interface utilisateur** :
  - Utilisation de Vue 3 avec `<script setup>`
  - Composants modulaires (authentification, chat, administration, ingestion, statistiques...)
- **Gestion de l'authentification** :
  - Connexion, inscription, changement de mot de passe
- **Gestion des chats** :
  - Envoi et affichage des messages
- **Administration** :
  - Gestion des départements, filières, modules, activités
- **Ingestion de documents** :
  - Formulaire d'import de documents
- **Visualisation de statistiques** :
  - Graphiques (BarChart, PieChart)
- **Navigation** :
  - Navbar, routing avec Vue Router
- **Gestion d'état** :
  - Utilisation de Pinia (stores)
- **Tests** :
  - (À compléter selon la stack de test utilisée)
- **Build pour la production** :
  ```bash
  npm run build
  # ou
  yarn build
  ```
  Les fichiers générés seront dans le dossier `dist/`.

## Structure du projet
- `src/components/` : Composants Vue (auth, chat, admin, etc.)
- `src/views/` : Pages principales
- `src/router/` : Configuration du routing
- `src/services/` : Appels API
- `src/stores/` : Stores Pinia
- `public/` : Fichiers statiques



## Liens utiles
- [Documentation Vue 3](https://vuejs.org/)
- [Documentation Vite](https://vitejs.dev/)
- [Pinia (gestion d'état)](https://pinia.vuejs.org/)

---
N'hésitez pas à ouvrir une issue pour toute question ou suggestion !
>>>>>>> 54544bd55cc319a89096b7e03467826462311e83
