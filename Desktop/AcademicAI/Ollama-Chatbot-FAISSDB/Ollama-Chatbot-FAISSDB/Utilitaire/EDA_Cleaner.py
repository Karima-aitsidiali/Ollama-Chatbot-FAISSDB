import re
import string
import emoji
import nltk
import os
from typing import List

# --- Configuration et Téléchargement des Ressources NLTK ---
# Définir un chemin pour les données NLTK.
# Il est recommandé d'utiliser un chemin accessible en écriture par votre application,
# surtout dans des environnements conteneurisés ou serverless.
# Par exemple, 'nltk_data' dans le répertoire courant de l'application.
NLTK_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'nltk_data')

# Ajouter le chemin aux chemins de recherche de NLTK
if NLTK_DATA_PATH not in nltk.data.path:
    nltk.data.path.append(NLTK_DATA_PATH)

# Créer le répertoire si non existant
if not os.path.exists(NLTK_DATA_PATH):
    os.makedirs(NLTK_DATA_PATH)
    print(f"Répertoire NLTK créé : {NLTK_DATA_PATH}")

# Téléchargement des ressources NLTK
# Utilisez download_dir pour spécifier où les données doivent être sauvegardées.
try:
    print("Tentative de téléchargement des ressources NLTK...")
    nltk.download('punkt', download_dir=NLTK_DATA_PATH, quiet=True)
    nltk.download('punkt_tab', download_dir=NLTK_DATA_PATH, quiet=True) # Ajout explicitement pour l'erreur
    nltk.download('stopwords', download_dir=NLTK_DATA_PATH, quiet=True)
    print("Ressources NLTK téléchargées avec succès.")
except Exception as e:
    print(f"Erreur lors du téléchargement des ressources NLTK : {str(e)}")
    # Relancer l'exception car sans ces ressources, le nettoyeur ne fonctionnera pas
    raise

# --- Classe TextCleaner ---
class TextCleaner:
    """Classe pour nettoyer et prétraiter le texte."""
    
    def __init__(self):
        # Initialise les stop words pour le français et l'anglais
        self.stop_words = set(nltk.corpus.stopwords.words('french') + nltk.corpus.stopwords.words('english'))
        # Initialise l'ensemble des caractères de ponctuation
        self.punctuation = set(string.punctuation)
        # Utilise le tokenizer de mots de NLTK
        self.tokenizer = nltk.tokenize.word_tokenize
    
    def to_lowercase(self, text: str) -> str:
        """Convertit le texte en minuscules."""
        return text.lower()
    
    def remove_punctuation(self, text: str) -> str:
        """Supprime la ponctuation du texte."""
        return ''.join(char for char in text if char not in self.punctuation)
    
    def remove_numbers(self, text: str) -> str:
        """Supprime les nombres du texte."""
        return re.sub(r'\d+', '', text)
    
    def convert_emojis_to_text(self, text: str) -> str:
        """Convertit les emojis en leur description textuelle (ex: 😊 -> :smiling_face_with_smiling_eyes:)."""
        return emoji.demojize(text)
    
    def remove_emojis(self, text: str) -> str:
        """Supprime tous les emojis du texte."""
        return emoji.replace_emoji(text, replace="")
    
    def remove_stopwords(self, text: str) -> str:
        """Supprime les mots vides (stop words) du texte."""
        # Tokenise le texte, puis filtre les mots qui sont des stop words
        tokens = self.tokenizer(text)
        return ' '.join(token for token in tokens if token not in self.stop_words)
    
    def remove_special_chars(self, text: str) -> str:
        """Supprime les caractères spéciaux (non alphabétiques et non espaces) du texte."""
        # Utilise une expression régulière pour conserver uniquement les lettres et les espaces
        return re.sub(r'[^a-zA-Z\s]', '', text)
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenise le texte en une liste de mots."""
        return self.tokenizer(text)

# --- Classe TextPipeline ---
class TextPipeline:
    """Pipeline pour appliquer une série de transformations sur le texte."""
    
    def __init__(self, cleaner: TextCleaner):
        """Initialise le pipeline avec une instance de TextCleaner."""
        self.cleaner = cleaner
    
    def process(self, text: str) -> str:
        """Applique une séquence de nettoyage au texte."""
        try:
            # Applique les transformations séquentiellement
            text = self.cleaner.to_lowercase(text)
            text = self.cleaner.remove_punctuation(text)
            text = self.cleaner.remove_numbers(text)
            text = self.cleaner.remove_stopwords(text)
            # text = self.cleaner.convert_emojis_to_text(text)  # Décommenter si nécessaire
            text = self.cleaner.remove_emojis(text)            # Supprime les emojis après ou sans conversion
            # text = self.cleaner.remove_special_chars(text)    # Décommenter si nécessaire

            # Retourne le texte nettoyé en supprimant les espaces de début/fin
            return text.strip()
        except Exception as e:
            print(f"Erreur dans le pipeline de nettoyage : {str(e)}")
            # Relance l'exception pour permettre une gestion d'erreur supérieure
            raise

