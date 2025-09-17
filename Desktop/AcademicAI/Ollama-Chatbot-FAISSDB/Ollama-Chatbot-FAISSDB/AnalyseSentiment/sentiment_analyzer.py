# import pandas as pd
# from ollama_api import OllamaAPI
# from sqlalchemy import create_engine
# import json
# import os
# import time
# import logging
# from dotenv import load_dotenv
# import re
# from textblob import TextBlob
# from langchain_groq import ChatGroq

# # Configuration du logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # --- CONFIGURATION ---
# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# DATABASE_URL = "sqlite:///./bdd/chatbot_metadata.db"
# SQL_QUERY = """
# SELECT ID, Département, Filière, Profile, "User", FeedBack, "timestamp"
# FROM "V_FeedBack"
# """

# class SimpleSentimentAnalyzer:
#     def __init__(self):
#         self.llm = None
#         if GROQ_API_KEY:
#             try:
#                 self.llm = ChatGroq(
#                     model_name="llama3-8b-8192",
#                     temperature=0,
#                     api_key=GROQ_API_KEY,
#                     max_retries=2,
#                     request_timeout=30,
#                     max_tokens=200
#                 )
#                 logger.info("LLM Groq initialisé avec succès")
#             except Exception as e:
#                 logger.warning(f"Impossible d'initialiser Groq: {e}")
#                 self.llm = None
    
#     def analyze_sentiment_rule_based(self, feedback_text):
#         """Analyse de sentiment basée sur des règles"""
#         feedback_lower = feedback_text.lower()
        
#         # Mots-clés pour détecter le contenu pédagogique
#         content_keywords = [
#             'contenu', 'cours', 'leçon', 'résumé', 'explication', 'pédagogique',
#             'matière', 'sujet', 'chapitre', 'module', 'formation', 'apprentissage',
#             'réponse', 'solution', 'information', 'connaissance', 'enseignement'
#         ]
        
#         # Mots-clés positifs
#         positive_keywords = [
#             'génial', 'super', 'magnifique', 'excellent', 'parfait', 'bien', 'bon',
#             'merci', 'formidable', 'fantastique', 'top', 'bravo', 'impressionnant',
#             'efficace', 'utile', 'clair', 'précis', 'complet', 'satisfait', 
#             'agréable', 'intéressant', 'captivant', 'engageant', 'instructif', 'utile', 'pratique',
#             'facile à comprendre', 'bien structuré', 'bien expliqué',
#             'très utile', 'très clair', 'très complet', 'très intéressant', 'très engageant'
#         ]
        
#         # Mots-clés négatifs  
#         negative_keywords = [
#             'mauvais', 'nul', 'horrible', 'décevant', 'problème', 'erreur',
#             'difficile', 'compliqué', 'confus', 'incompréhensible', 'long',
#             'court', 'bref', 'insuffisant', 'pas convaincu',
#             'peu clair', 'peu précis', 'peu complet', 'peu intéressant',
#             'peu engageant', 'peu utile', 'peu pratique', 'pas utile',
#             'pas pratique', 'pas efficace', 'pas satisfaisant', 'pas agréable',
#         ]
        
#         # Mots-clés neutres/critiques constructives
#         neutral_keywords = [
#             'correcte', 'acceptable', 'moyen', 'peut mieux faire', 'améliorer',
#             'manque de', 'besoin de', 'pourrait être mieux', 'manque de clarté',
#             'manque de détails', 'manque d''exemples', 'manque de structure'

#         ]
        
#         # Vérifier si le contenu pédagogique est mentionné
#         has_content = any(keyword in feedback_lower for keyword in content_keywords)
        
#         if not has_content:
#             return {"aspect": "Contenu pédagogique", "polarity": "non mentionné"}
        
#         # Compter les occurrences
#         positive_count = sum(1 for keyword in positive_keywords if keyword in feedback_lower)
#         negative_count = sum(1 for keyword in negative_keywords if keyword in feedback_lower)
#         neutral_count = sum(1 for keyword in neutral_keywords if keyword in feedback_lower)
        
#         # Analyser les patterns spécifiques
#         if 'trop long' in feedback_lower or 'trop brève' in feedback_lower:
#             negative_count += 1
        
#         if 'préfère' in feedback_lower and 'résumé' in feedback_lower:
#             neutral_count += 1
        
#         # Déterminer la polarité
#         if positive_count > negative_count and positive_count > neutral_count:
#             polarity = "positive"
#         elif negative_count > positive_count and negative_count > neutral_count:
#             polarity = "négative"
#         elif neutral_count > 0:
#             polarity = "neutre"
#         else:
#             polarity = "neutre"
        
#         logger.debug(f"Analyse: pos={positive_count}, neg={negative_count}, neu={neutral_count} -> {polarity}")
#         return {"aspect": "Contenu pédagogique", "polarity": polarity}
    
#     def analyze_sentiment_textblob(self, feedback_text):
#         """Analyse de sentiment avec TextBlob comme backup"""
#         try:
#             blob = TextBlob(feedback_text)
#             sentiment_score = blob.sentiment.polarity
            
#             # Vérifier si le contenu pédagogique est mentionné
#             content_keywords = ['contenu', 'cours', 'réponse', 'explication', 'résumé']
#             has_content = any(keyword in feedback_text.lower() for keyword in content_keywords)
            
#             if not has_content:
#                 return {"aspect": "Contenu pédagogique", "polarity": "non mentionné"}
            
#             if sentiment_score > 0.1:
#                 polarity = "positive"
#             elif sentiment_score < -0.1:
#                 polarity = "négative"
#             else:
#                 polarity = "neutre"
                
#             return {"aspect": "Contenu pédagogique", "polarity": polarity}
#         except:
#             return self.analyze_sentiment_rule_based(feedback_text)
    
#     def analyze_sentiment_llm(self, feedback_text):
#         """Analyse avec LLM si disponible"""
#         if not self.llm:
#             return None
            
#         try:
#             prompt = f"""Analyse le sentiment de ce feedback concernant le contenu pédagogique.
            
# Feedback: "{feedback_text}"

# Réponds UNIQUEMENT avec un JSON valide:
# {{"aspect": "Contenu pédagogique", "polarity": "positive/négative/neutre/non mentionné"}}

# Si le feedback ne mentionne pas le contenu pédagogique, utilise "non mentionné".
# """
            
#             #response = self.llm.invoke(prompt)
#             ollama_api = OllamaAPI()
#             response = ollama_api.chat_with_ollama(prompt)
#             response_text = response.content if hasattr(response, 'content') else str(response)
            
#             # Extraire le JSON
#             start_idx = response_text.find('{')
#             end_idx = response_text.rfind('}')
            
#             if start_idx != -1 and end_idx != -1:
#                 json_str = response_text[start_idx:end_idx+1]
#                 result = json.loads(json_str)
                
#                 if 'aspect' in result and 'polarity' in result:
#                     return result
                    
#         except Exception as e:
#             logger.warning(f"Erreur LLM: {e}")
            
#         return None
    
#     def analyze_single_feedback(self, feedback_text):
#         """Analyse un feedback avec plusieurs méthodes en cascade"""
#         if not feedback_text or not feedback_text.strip():
#             return {"aspect": "Contenu pédagogique", "polarity": "vide"}
        
#         # Nettoyer le feedback
#         cleaned_feedback = feedback_text.strip()[:500]
        
#         # Méthode 1: Essayer avec LLM
#         if self.llm:
#             llm_result = self.analyze_sentiment_llm(cleaned_feedback)
#             if llm_result:
#                 logger.info(f"Analyse LLM réussie: {llm_result}")
#                 return llm_result
        
#         # Méthode 2: Analyse basée sur des règles (plus fiable)
#         rule_result = self.analyze_sentiment_rule_based(cleaned_feedback)
#         logger.info(f"Analyse par règles: {rule_result}")
#         return rule_result
    
#     def fetch_feedbacks(self):
#         """Récupérer les feedbacks depuis la base de données"""
#         engine = create_engine(DATABASE_URL)
#         try:
#             with engine.connect() as connection:
#                 df = pd.read_sql_query(SQL_QUERY, connection)
#             logger.info(f"{len(df)} feedbacks récupérés")
#             return df
#         except Exception as e:
#             logger.error(f"Erreur base de données: {e}")
#             return pd.DataFrame()
    
#     def analyze_all_feedbacks(self):
#         """Analyser tous les feedbacks"""
#         feedbacks_df = self.fetch_feedbacks()
        
#         if feedbacks_df.empty:
#             logger.warning("Aucun feedback trouvé")
#             return pd.DataFrame()
        
#         results = []
#         total_feedbacks = len(feedbacks_df)
        
#         logger.info(f"Début de l'analyse de {total_feedbacks} feedbacks")
        
#         for idx, row in feedbacks_df.iterrows():
#             logger.info(f"\n{'='*50}")
#             logger.info(f"Analyse du feedback n°{idx + 1}/{total_feedbacks} de {row['User']}")
            
#             if pd.isna(row['FeedBack']) or not row['FeedBack'].strip():
#                 sentiment = {"aspect": "Contenu pédagogique", "polarity": "vide"}
#             else:
#                 feedback = row['FeedBack']
#                 logger.info(f"Feedback: '{feedback[:100]}{'...' if len(feedback) > 100 else ''}'")
#                 sentiment = self.analyze_single_feedback(feedback)
            
#             # Enrichir les données
#             enriched = row.to_dict()
#             enriched.update(sentiment)
#             results.append(enriched)
            
#             logger.info(f"-> Résultat: {sentiment}")
            
#             # Petite pause pour éviter la surcharge
#             time.sleep(0.1)
        
#         results_df = pd.DataFrame(results)
        
#         # Sauvegarder les résultats
#         try:
#             # results_df.to_csv("feedbacks_analyzed.csv", index=False, encoding='utf-8-sig')
#             # logger.info("Résultats sauvegardés dans feedbacks_analyzed.csv")
            
#             # Afficher un résumé
#             polarity_counts = results_df['polarity'].value_counts()
#             logger.info(f"Résumé des polarités:\n{polarity_counts}")
            
#         except Exception as e:
#             logger.error(f"Erreur lors de la sauvegarde: {e}")
        
#         return results_df

import pandas as pd
from ollama_api import OllamaAPI
from sqlalchemy import create_engine, text
import json
import os
import time
import logging
from dotenv import load_dotenv
from textblob import TextBlob
from langchain_groq import ChatGroq

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = "sqlite:///./bdd/chatbot_metadata.db"

SQL_QUERY = """
SELECT id as ID, Département, Filière, Profile, "User", FeedBack, "timestamp"
FROM "V_FeedBack"
WHERE polarity IS NULL
"""

class SimpleSentimentAnalyzer:
    def __init__(self):
        self.llm = None
        if GROQ_API_KEY:
            try:
                self.llm = ChatGroq(
                    model_name="llama3-8b-8192",
                    temperature=0,
                    api_key=GROQ_API_KEY,
                    max_retries=2,
                    request_timeout=30,
                    max_tokens=200
                )
                logger.info("LLM Groq initialisé avec succès")
            except Exception as e:
                logger.warning(f"Impossible d'initialiser Groq: {e}")
                self.llm = None

    def analyze_sentiment_rule_based(self, feedback_text):
        feedback_lower = feedback_text.lower()
        content_keywords = [
            'contenu', 'cours', 'leçon', 'résumé', 'explication', 'pédagogique',
            'matière', 'sujet', 'chapitre', 'module', 'formation', 'apprentissage',
            'réponse', 'solution', 'information', 'connaissance', 'enseignement'
        ]
        positive_keywords = [
            'génial', 'super', 'magnifique', 'excellent', 'parfait', 'bien', 'bon',
            'merci', 'formidable', 'fantastique', 'top', 'bravo', 'impressionnant',
            'efficace', 'utile', 'clair', 'précis', 'complet', 'satisfait', 
            'agréable', 'intéressant', 'captivant', 'engageant', 'instructif', 'pratique',
            'facile à comprendre', 'bien structuré', 'bien expliqué',
            'très utile', 'très clair', 'très complet', 'très intéressant', 'très engageant'
        ]
        negative_keywords = [
            'mauvais', 'nul', 'horrible', 'décevant', 'problème', 'erreur',
            'difficile', 'compliqué', 'confus', 'incompréhensible', 'long',
            'court', 'bref', 'insuffisant', 'pas convaincu',
            'peu clair', 'peu précis', 'peu complet', 'peu intéressant',
            'peu engageant', 'peu utile', 'peu pratique', 'pas utile',
            'pas pratique', 'pas efficace', 'pas satisfaisant', 'pas agréable',
        ]
        neutral_keywords = [
            'correcte', 'acceptable', 'moyen', 'peut mieux faire', 'améliorer',
            'manque de', 'besoin de', 'pourrait être mieux', 'manque de clarté',
            'manque de détails', "manque d'exemples", 'manque de structure'
        ]
        has_content = any(keyword in feedback_lower for keyword in content_keywords)
        if not has_content:
            return {"aspect": "Contenu pédagogique", "polarity": "non mentionné"}
        positive_count = sum(1 for keyword in positive_keywords if keyword in feedback_lower)
        negative_count = sum(1 for keyword in negative_keywords if keyword in feedback_lower)
        neutral_count = sum(1 for keyword in neutral_keywords if keyword in feedback_lower)
        if 'trop long' in feedback_lower or 'trop brève' in feedback_lower:
            negative_count += 1
        if 'préfère' in feedback_lower and 'résumé' in feedback_lower:
            neutral_count += 1
        if positive_count > negative_count and positive_count > neutral_count:
            polarity = "positive"
        elif negative_count > positive_count and negative_count > neutral_count:
            polarity = "négative"
        elif neutral_count > 0:
            polarity = "neutre"
        else:
            polarity = "neutre"
        logger.debug(f"Analyse: pos={positive_count}, neg={negative_count}, neu={neutral_count} -> {polarity}")
        return {"aspect": "Contenu pédagogique", "polarity": polarity}

    def analyze_sentiment_textblob(self, feedback_text):
        try:
            blob = TextBlob(feedback_text)
            sentiment_score = blob.sentiment.polarity
            content_keywords = ['contenu', 'cours', 'réponse', 'explication', 'résumé']
            has_content = any(keyword in feedback_text.lower() for keyword in content_keywords)
            if not has_content:
                return {"aspect": "Contenu pédagogique", "polarity": "non mentionné"}
            if sentiment_score > 0.1:
                polarity = "positive"
            elif sentiment_score < -0.1:
                polarity = "négative"
            else:
                polarity = "neutre"
            return {"aspect": "Contenu pédagogique", "polarity": polarity}
        except:
            return self.analyze_sentiment_rule_based(feedback_text)

    def analyze_sentiment_llm(self, feedback_text):
        if not self.llm:
            return None
        try:
            prompt = f"""Analyse le sentiment de ce feedback concernant le contenu pédagogique.

Feedback: "{feedback_text}"

Réponds UNIQUEMENT avec un JSON valide:
{{"aspect": "Contenu pédagogique", "polarity": "positive/négative/neutre/non mentionné"}}

Si le feedback ne mentionne pas le contenu pédagogique, utilise "non mentionné".
"""
            ollama_api = OllamaAPI()
            response = ollama_api.chat_with_ollama(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx+1]
                result = json.loads(json_str)
                if 'aspect' in result and 'polarity' in result:
                    return result
        except Exception as e:
            logger.warning(f"Erreur LLM: {e}")
        return None

    def analyze_single_feedback(self, feedback_text):
        if not feedback_text or not feedback_text.strip():
            return {"aspect": "Contenu pédagogique", "polarity": "vide"}
        cleaned_feedback = feedback_text.strip()[:500]
        if self.llm:
            llm_result = self.analyze_sentiment_llm(cleaned_feedback)
            if llm_result:
                logger.info(f"Analyse LLM réussie: {llm_result}")
                return llm_result
        rule_result = self.analyze_sentiment_rule_based(cleaned_feedback)
        logger.info(f"Analyse par règles: {rule_result}")
        return rule_result

    def fetch_feedbacks(self):
        engine = create_engine(DATABASE_URL)
        try:
            with engine.connect() as connection:
                df = pd.read_sql_query(SQL_QUERY, connection)
            logger.info(f"{len(df)} feedbacks à traiter récupérés")
            return df
        except Exception as e:
            logger.error(f"Erreur base de données: {e}")
            return pd.DataFrame()

    def update_feedback_polarity(self, feedback_id, polarity):
        engine = create_engine(DATABASE_URL)
        try:
            with engine.begin() as connection:  # begin() = commit auto
                connection.execute(
                    text("UPDATE feedbacks SET polarity = :polarity WHERE id = :id"),
                    {"polarity": polarity, "id": feedback_id}
                )
            logger.info(f"Feedback ID {feedback_id} mis à jour avec la polarité '{polarity}'")
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du feedback ID {feedback_id}: {e}")

    def analyze_and_update_feedbacks(self):
        feedbacks_df = self.fetch_feedbacks()
        if feedbacks_df.empty:
            logger.warning("Aucun feedback à traiter")
            # Recharge quand même pour le dashboard
            return self.reload_feedbacks_for_dashboard()
        total_feedbacks = len(feedbacks_df)
        logger.info(f"Début de l'analyse de {total_feedbacks} feedbacks")
        for idx, row in feedbacks_df.iterrows():
            logger.info(f"\n{'='*50}")
            logger.info(f"Analyse du feedback n°{idx + 1}/{total_feedbacks} de {row['User']}")
            if pd.isna(row['FeedBack']) or not row['FeedBack'].strip():
                sentiment = {"aspect": "Contenu pédagogique", "polarity": "vide"}
            else:
                feedback = row['FeedBack']
                logger.info(f"Feedback: '{feedback[:100]}{'...' if len(feedback) > 100 else ''}'")
                sentiment = self.analyze_single_feedback(feedback)
            self.update_feedback_polarity(row['ID'], sentiment["polarity"])
            logger.info(f"-> Résultat: {sentiment}")
            time.sleep(0.1)
        # Recharge les feedbacks à jour pour le dashboard
        return self.reload_feedbacks_for_dashboard()

    def reload_feedbacks_for_dashboard(self):
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            analyzed_df = pd.read_sql_query(
                """
                SELECT "ID", Département, Filière, Profile, "User", polarity, "timestamp"
                FROM "V_FeedBack"
                """,
                connection
            )
        analyzed_df['polarity'] = analyzed_df['polarity'].fillna('non mentionné')
        return analyzed_df