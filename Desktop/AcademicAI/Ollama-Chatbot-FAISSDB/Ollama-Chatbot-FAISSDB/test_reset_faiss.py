#!/usr/bin/env python3
"""
Script de test pour la fonctionnalité de réinitialisation FAISS.
Ce script teste la fonction reset_faiss_database() directement et via l'API.
"""

import os
import sys
import requests
import json

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ollama_api import OllamaAPI
from rag_chatbot import RAGChatbot

def test_reset_function_directly():
    """Test de la fonction reset_faiss_database() directement"""
    print("=== Test de la fonction reset_faiss_database() directement ===")
    
    try:
        # Initialiser le chatbot
        ollama_api = OllamaAPI()
        chatbot = RAGChatbot(ollama_api)
        
        print("Chatbot initialisé avec succès")
        print(f"Nombre de vecteurs avant réinitialisation : {chatbot.index.ntotal}")
        print(f"Nombre de métadonnées avant réinitialisation : {len(chatbot.metadata)}")
        
        # Appeler la fonction de réinitialisation
        result = chatbot.reset_faiss_database()
        
        # Afficher le résultat
        print("\n--- Résultat de la réinitialisation ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Vérifier l'état après réinitialisation
        print(f"\nNombre de vecteurs après réinitialisation : {chatbot.index.ntotal}")
        print(f"Nombre de métadonnées après réinitialisation : {len(chatbot.metadata)}")
        
        if result["status"] == "success":
            print("✅ Test réussi : La fonction fonctionne correctement")
            return True
        else:
            print("❌ Test échoué : La fonction a retourné une erreur")
            return False
            
    except Exception as e:
        print(f"❌ Test échoué avec exception : {e}")
        return False

def test_reset_api_endpoint():
    """Test de l'endpoint API POST /reset-faiss"""
    print("\n\n=== Test de l'endpoint API POST /reset-faiss ===")
    
    # URL de l'API (adapter selon votre configuration)
    api_url = "http://localhost:8000/reset-faiss"
    
    try:
        # Faire un appel POST à l'endpoint
        response = requests.post(api_url)
        
        print(f"Code de statut HTTP : {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("--- Réponse de l'API ---")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print("✅ Test API réussi")
            return True
        else:
            print(f"❌ Test API échoué - Code d'erreur : {response.status_code}")
            try:
                error_detail = response.json()
                print("Détail de l'erreur :", error_detail)
            except:
                print("Réponse brute :", response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API. Assurez-vous que le serveur FastAPI est démarré sur localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test API échoué avec exception : {e}")
        return False

if __name__ == "__main__":
    print("Script de test pour la réinitialisation FAISS")
    print("=" * 50)
    
    # Test de la fonction directement
    direct_test_success = test_reset_function_directly()
    
    # Test de l'API (optionnel - nécessite que le serveur soit en cours d'exécution)
    print("\n" + "="*50)
    print("Pour tester l'endpoint API, démarrez le serveur FastAPI avec :")
    print("uvicorn api.main:app --reload")
    print("Puis relancez ce script ou appelez l'endpoint directement.")
    
    # Déscommentez les lignes suivantes pour tester l'API automatiquement
    # api_test_success = test_reset_api_endpoint()
    
    print("\n" + "="*50)
    if direct_test_success:
        print("✅ Tous les tests directs ont réussi !")
    else:
        print("❌ Certains tests ont échoué.")