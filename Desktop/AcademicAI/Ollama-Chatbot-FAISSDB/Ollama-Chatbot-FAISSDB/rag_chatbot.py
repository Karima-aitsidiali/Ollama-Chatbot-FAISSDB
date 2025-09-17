import sys
import time
import os, re
import pickle
import faiss
import numpy as np
from colorama import Fore, Style
from sentence_transformers import SentenceTransformer
# Supposons que OllamaAPI, FileProcessor, FilterManager sont correctement importés
from ollama_api import OllamaAPI
from Utilitaire.file_processor import FileProcessor
from Utilitaire.filter_manager import FilterManager
from Utilitaire.promptbuilder import PromptBuilder

import traceback # Pour un meilleur débogage

class RAGChatbot:
    
    def __init__(self, ollama_api, chunk_size=384, chunk_overlap=96, faiss_index_file='./vector_store/faiss_index.faiss', metadata_file='./vector_store/metadata.pickle', hashes_file='./vector_store/hashes.pickle'):
        self.ollama_api = ollama_api
        self.embedding_model = SentenceTransformer('BAAI/bge-base-en-v1.5')
        self.file_processor = FileProcessor(chunk_size, chunk_overlap)
        self.dimension = 768  # Correct pour BAAI/bge-base-en-v1.5
        self.MCNoeud = 32
        self.efSearch = 100
        self.efConstruction = 80
        self.faiss_index_file = faiss_index_file
        self.metadata_file = metadata_file
        self.hashes_file = hashes_file

        self.index = self.load_or_initialize_index()
        self.metadata = self.load_or_initialize_metadata() # C'est une liste de dictionnaires
        self.load_processed_hashes()

    def normalize_embedding(self, embedding):
        norm = np.linalg.norm(embedding)
        return embedding / norm if norm > 0 else embedding

    def load_or_initialize_index(self):
        if os.path.exists(self.faiss_index_file):
            # print(f"Chargement de l'index Faiss depuis {self.faiss_index_file}")
            return faiss.read_index(self.faiss_index_file)
        else:
            
            
            index = faiss.IndexHNSWFlat(self.dimension, self.MCNoeud, faiss.METRIC_INNER_PRODUCT)
            index.hnsw.efSearch = self.efSearch
            index.hnsw.efConstruction = self.efConstruction
            return index

    def load_or_initialize_metadata(self):
        if os.path.exists(self.metadata_file):
            #print(f"Chargement des métadonnées depuis {self.metadata_file}")
            with open(self.metadata_file, 'rb') as f:
                return pickle.load(f)
        else:
            print("Initialisation d'une nouvelle liste de métadonnées.")
            return []

    def load_processed_hashes(self):
        if os.path.exists(self.hashes_file):
            #print(f"Chargement des hashes traités depuis {self.hashes_file}")
            with open(self.hashes_file, 'rb') as f:
                self.file_processor.processed_hashes = pickle.load(f)
        else:
            #print("Initialisation d'un nouvel ensemble de hashes traités.")
            # Assurez-vous que processed_hashes est initialisé dans FileProcessor si le fichier n'existe pas
            if not hasattr(self.file_processor, 'processed_hashes'):
                 self.file_processor.processed_hashes = set()


    def save_state(self):
        print("Sauvegarde de l'état (index, métadonnées, hashes)...")
        os.makedirs(os.path.dirname(self.faiss_index_file), exist_ok=True)
        faiss.write_index(self.index, self.faiss_index_file)
        with open(self.metadata_file, 'wb') as f:
            pickle.dump(self.metadata, f)
        with open(self.hashes_file, 'wb') as f:
            pickle.dump(self.file_processor.processed_hashes, f)
        print("État sauvegardé.")

    def reset_faiss_database(self):
        """
        Vide complètement la base vectorielle FAISS en supprimant tous les fichiers
        d'index existants et réinitialise avec un nouvel index vide.
        
        Returns:
            dict: Message de confirmation avec le statut de l'opération
        """
        try:
            print("Début de la réinitialisation de la base vectorielle FAISS...")
            
            # Liste des fichiers à supprimer
            files_to_remove = [
                self.faiss_index_file,
                self.metadata_file, 
                self.hashes_file
            ]
            
            # Supprimer les fichiers existants s'ils existent
            removed_files = []
            for file_path in files_to_remove:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        removed_files.append(file_path)
                        print(f"Fichier supprimé : {file_path}")
                    except OSError as e:
                        print(f"Erreur lors de la suppression de {file_path} : {e}")
                        raise
            
            # Réinitialiser l'index FAISS avec un nouvel index vide
            print("Création d'un nouvel index FAISS vide...")
            self.index = faiss.IndexHNSWFlat(self.dimension, self.MCNoeud, faiss.METRIC_INNER_PRODUCT)
            self.index.hnsw.efSearch = self.efSearch
            self.index.hnsw.efConstruction = self.efConstruction
            
            # Réinitialiser les métadonnées
            self.metadata = []
            
            # Réinitialiser les hashes traités
            self.file_processor.processed_hashes = set()
            
            # Supprimer les métadonnées de la base SQLite (si nécessaire)
            try:
                FilterManager.clear_all_metadata_sqlite()
                print("Métadonnées SQLite vidées")
            except Exception as e:
                print(f"Avertissement : Erreur lors du vidage des métadonnées SQLite : {e}")
            
            # Sauvegarder l'état vide
            self.save_state()
            
            result_message = {
                "status": "success",
                "message": "Base vectorielle FAISS réinitialisée avec succès",
                "details": {
                    "removed_files": removed_files,
                    "total_vectors_before": "Inconnu (fichiers supprimés)",
                    "total_vectors_after": 0,
                    "metadata_count": 0,
                    "processed_hashes_count": 0
                }
            }
            
            print("Réinitialisation FAISS terminée avec succès")
            return result_message
            
        except Exception as e:
            error_message = {
                "status": "error", 
                "message": f"Erreur lors de la réinitialisation FAISS : {str(e)}",
                "details": {
                    "error_type": type(e).__name__
                }
            }
            print(f"Erreur lors de la réinitialisation FAISS : {e}")
            traceback.print_exc()
            return error_message

    def ingestion_file(self, base_filename, file_content, departement_id, filiere_id, module_id, activite_id, profile_id, user_id):
        try:
            chunks, file_hash = self.file_processor.process_file(base_filename, file_content)
            if chunks is None:
                print(f"Traitement de {base_filename} annulé (déjà traité ou contenu non valide).")
                if file_hash:
                    raise ValueError(f"Le fichier {base_filename} (hash: {file_hash}) a déjà été traité.")
                else:
                    raise ValueError(f"Le contenu du fichier {base_filename} n'a pas pu être traité ou était vide.")
            if not chunks:
                print(f"Aucun chunk extrait de {base_filename}. L'indexation est annulée pour ce fichier.")
                return

            embeddings = []
            for chunk_text_content in chunks:
                # Pour BGE, il est recommandé de ne pas ajouter d'instruction aux documents lors de l'indexation.
                embedding = self.embedding_model.encode([chunk_text_content], normalize_embeddings=True)[0]
                # La normalisation est déjà faite par normalize_embeddings=True
                # normalized_embedding = self.normalize_embedding(embedding) # Plus besoin si normalize_embeddings=True
                embeddings.append(embedding) # Utiliser directement l'embedding normalisé

            if not embeddings:
                print(f"Aucun embedding n'a pu être généré pour les chunks de {base_filename}.")
                raise ValueError(f"Échec de la génération d'embeddings pour {base_filename}.")

            embeddings_np = np.array(embeddings, dtype='float32')
            start_index = self.index.ntotal
            self.index.add(embeddings_np)

            for i, chunk_text_content in enumerate(chunks):
                current_global_chunk_index = start_index + i
                self.metadata.append({
                    "file_hash": file_hash,
                    "original_filename": base_filename,
                    "faiss_index": current_global_chunk_index,
                    "chunk_text": chunk_text_content,
                    # Stocker aussi les filtres pour un accès direct si nécessaire, ou compter sur la DB
                    "departement_id": departement_id,
                    "filiere_id": filiere_id,
                    "module_id": module_id,
                    "activite_id": activite_id,
                    "profile_id": profile_id,
                    "user_id": user_id
                })
                FilterManager.insert_metadata_sqlite(
                    base_filename=base_filename, file_hash=file_hash,
                    chunk_index=current_global_chunk_index, chunk_text=chunk_text_content,
                    departement_id=departement_id, filiere_id=filiere_id, module_id=module_id,
                    activite_id=activite_id, profile_id=profile_id, user_id=user_id
                )
            self.save_state()
            print(f"Fichier {base_filename} indexé. {len(chunks)} chunks ajoutés. L'index Faiss contient maintenant {self.index.ntotal} vecteurs.")
        except ValueError as ve:
            print(f"Erreur de valeur lors de l'indexation de {base_filename} : {str(ve)}")
            raise
        except Exception as e:
            print(f"Erreur inattendue lors de l'indexation de {base_filename} : {str(e)}")
            traceback.print_exc()
            raise

    # --- MMR (Maximal Marginal Relevance) implementation optionnelle ---
    def mmr(self, query_embedding, candidate_embeddings, k=3, lambda_param=0.5):
        """
        Maximal Marginal Relevance (MMR) pour diversifier les chunks sélectionnés.
        query_embedding: np.array de shape (dim,)
        candidate_embeddings: np.array de shape (n, dim)
        k: nombre de chunks à retourner
        lambda_param: balance entre pertinence et diversité (0.0 = diversité max, 1.0 = pertinence max)
        """
        selected = []
        selected_indices = []
        candidate_indices = list(range(len(candidate_embeddings)))
        query_embedding = query_embedding.reshape(1, -1)
        candidate_embeddings = np.array(candidate_embeddings)
        # Similarité entre la requête et chaque chunk
        sim_to_query = np.dot(candidate_embeddings, query_embedding.T).flatten()
        for _ in range(min(k, len(candidate_embeddings))):
            if not selected:
                idx = int(np.argmax(sim_to_query))
                selected.append(candidate_embeddings[idx])
                selected_indices.append(idx)
                candidate_indices.remove(idx)
            else:
                max_score = -np.inf
                max_idx = -1
                for idx in candidate_indices:
                    # Pertinence
                    relevance = sim_to_query[idx]
                    # Diversité : max similarité avec les déjà sélectionnés
                    diversity = max([np.dot(candidate_embeddings[idx], s) for s in selected])
                    mmr_score = lambda_param * relevance - (1 - lambda_param) * diversity
                    if mmr_score > max_score:
                        max_score = mmr_score
                        max_idx = idx
                selected.append(candidate_embeddings[max_idx])
                selected_indices.append(max_idx)
                candidate_indices.remove(max_idx)
        return selected_indices

    # --- Recherche de contexte avec option MMR (Maximal Marginal Relevance) ---
    def find_relevant_context(self, user_query,
                              departement_id=None, filiere_id=None,
                              top_k=3, similarity_threshold=0.65, use_mmr=False, mmr_lambda=0.5):
        """
        Recherche les chunks les plus pertinents pour une requête utilisateur,
        en utilisant les ID Faiss globaux filtrés et en reconstruisant les vecteurs correctement.
        """
        try:
            # Pour BGE, il est souvent recommandé d'ajouter une instruction aux requêtes.
            # Consultez la documentation du modèle BGE spécifique.
            # Pour 'BAAI/bge-base-en-v1.5', l'instruction est souvent:
            # "Represent this sentence for searching relevant passages: "
            # Cependant, SentenceTransformer peut le gérer implicitement pour certains modèles.
            # Si vous utilisez normalize_embeddings=True, la normalisation est déjà faite.
            query_embedding = self.embedding_model.encode([user_query], normalize_embeddings=True)[0]
            # normalized_query = self.normalize_embedding(query_embedding).reshape(1, -1) # Plus besoin
            normalized_query = query_embedding.reshape(1, -1)
        except Exception as e:
            print(f"Erreur lors de la génération de l'embedding de la requête: {e}")
            traceback.print_exc()
            return None

        if not hasattr(self.index, 'ntotal') or self.index.ntotal == 0:
            print("Aucun contexte indexé dans Faiss ou l'index n'est pas correctement initialisé.")
            return None

        try:
            allowed_faiss_ids = FilterManager.get_allowed_indices(
                departement_id, filiere_id
            )
        except Exception as e:
            print(f"Erreur lors de la récupération des IDs autorisés depuis FilterManager: {e}")
            traceback.print_exc()
            return None

        if not allowed_faiss_ids:
            print("Aucun chunk autorisé trouvé pour ce contexte académique et ces filtres.")
            return None

        allowed_faiss_ids_array = np.array(list(allowed_faiss_ids), dtype='int64')
        valid_ids_for_reconstruction = np.array(
            [fid for fid in allowed_faiss_ids_array if 0 <= fid < self.index.ntotal],
            dtype='int64'
        )

        if len(valid_ids_for_reconstruction) == 0:
            print("Aucun ID Faiss autorisé n'est actuellement valide dans l'index principal.")
            return None

        sub_vectors_list = []
        try:
            # Pour IndexHNSWFlat, les vecteurs sont dans 'storage' qui est un IndexFlat.
            # Si self.index.storage n'existe pas ou est None, il y a un problème avec l'init de l'index HNSW.
            if not hasattr(self.index, 'storage') or self.index.storage is None:
                 print("L'index HNSW ne semble pas avoir de 'storage' valide pour la reconstruction.")
                 return None
            
            reconstruction_source = self.index.storage
            for vector_id in valid_ids_for_reconstruction:
                reconstructed_vec = reconstruction_source.reconstruct(int(vector_id))
                sub_vectors_list.append(reconstructed_vec)

            if not sub_vectors_list:
                print("La liste des vecteurs reconstruits est vide.")
                return None
            sub_vectors = np.array(sub_vectors_list, dtype='float32')

        except AttributeError as ae:
            print(f"Erreur d'attribut lors de la reconstruction (vérifiez type d'index): {ae}")
            traceback.print_exc()
            return None
        except Exception as e:
            print(f"Erreur inattendue lors de la reconstruction des vecteurs: {e}")
            traceback.print_exc()
            return None

        if sub_vectors.shape[0] == 0:
            print("Aucun vecteur n'a pu être reconstruit (shape[0] est 0).")
            return None

        try:
            # Le sous-index doit utiliser la même métrique que l'index principal si on compare les scores
            # Si l'index HNSW utilise METRIC_INNER_PRODUCT, le sous-index aussi.
            sub_index = faiss.IndexFlatIP(self.dimension)
            sub_index.add(sub_vectors)
        except Exception as e:
            print(f"Erreur lors de la création/ajout au sous-index Faiss: {e}")
            traceback.print_exc()
            return None

        try:
            k_search = min(top_k * 5 if use_mmr else top_k, sub_index.ntotal)
            if k_search == 0:
                print("Le sous-index est vide, impossible de rechercher.")
                return None
            distances, local_indices_in_sub = sub_index.search(normalized_query, k_search)
        except Exception as e:
            print(f"Erreur lors de la recherche sur le sous-index Faiss: {e}")
            traceback.print_exc()
            return None

        # Récupérer les embeddings des candidats pour MMR
        candidate_embeddings = [sub_vectors[i] for i in local_indices_in_sub[0] if i >= 0 and distances[0][list(local_indices_in_sub[0]).index(i)] >= similarity_threshold]
        candidate_indices = [i for i in local_indices_in_sub[0] if i >= 0 and distances[0][list(local_indices_in_sub[0]).index(i)] >= similarity_threshold]

        if use_mmr and candidate_embeddings:
            mmr_indices = self.mmr(normalized_query.flatten(), candidate_embeddings, k=top_k, lambda_param=mmr_lambda)
            selected_indices = [candidate_indices[i] for i in mmr_indices]
        else:
            selected_indices = candidate_indices[:top_k]

        relevant_chunks_texts = []
        for i in selected_indices:
            global_faiss_id = valid_ids_for_reconstruction[i]
            chunk_data = None
            for meta_item in self.metadata:
                if meta_item.get("faiss_index") == global_faiss_id:
                    chunk_data = meta_item
                    break
            if chunk_data and 'chunk_text' in chunk_data:
                relevant_chunks_texts.append(chunk_data['chunk_text'])
                print(f"Debug: Chunk pertinent trouvé: ID={global_faiss_id}")
            else:
                print(f"Attention : Métadonnées ou texte du chunk introuvables pour l'ID Faiss global {global_faiss_id}")

        if not relevant_chunks_texts:
            print("Aucun chunk pertinent trouvé (seuil de similarité non atteint ou problème de métadonnées).")
            return None
        return relevant_chunks_texts

    # ... (autres méthodes : clean_llm_response, generate_response, etc. restent inchangées) ...
    def clean_llm_response(self, response: str) -> str:
    # Extraire uniquement le texte après la dernière occurrence de '</'
        if '</' in response:
            response = response.split('</')[-1]

        # Nettoyage supplémentaire
        cleaned = re.sub(r"<?think>", "", response, flags=re.DOTALL | re.IGNORECASE)
        cleaned = re.sub(r"</?think>", "", cleaned, flags=re.IGNORECASE)
        return cleaned.strip()
    
    SQLITE_DB_PATH = "./bdd/chatbot_metadata.db"
    
    def generate_response(self, user_query, user_id, profile_id, departement_id, filiere_id, use_mmr=False):
        INVITE_PROFILE_ID = 5

        is_invite = (profile_id == INVITE_PROFILE_ID)
        if is_invite:
            departement_id = 1
            filiere_id = 3

        context_chunks = self.find_relevant_context(
            user_query, departement_id, filiere_id, top_k=3, similarity_threshold=0.65, use_mmr=use_mmr
        )

        if context_chunks:
            context_text = "\n".join(context_chunks)
            if PromptBuilder.is_qcm_request(user_query):
                prompt_text = PromptBuilder.build_qcm_prompt(context_text, user_query)
            elif "résumé" in user_query.lower() or "synthèse" in user_query.lower():
                prompt_text = PromptBuilder.build_summary_prompt(context_text, user_query)
            else:
                prompt_text = PromptBuilder.build_standard_prompt(context_text, user_query)

            # Ajout de la consigne spéciale pour l'invité
            if is_invite:
                prompt_text = (
                    "⚠️ **Mode invité activé :**\n"
                    "Tu dois répondre **uniquement** à partir des informations fournies par le département Scolarité.\n"
                    "Si la question ne concerne pas le département Scolarité, ou si tu n’as pas l’information dans le contexte, réponds exactement :\n"
                    "\"Je ne peux répondre qu’aux questions relatives au département Scolarité.\"\n"
                    "N’ajoute rien d’autre, n’explique pas, ne propose pas de ressources, ne donne aucune information supplémentaire.\n"
                    "N’utilise **aucune autre information**, même si elle est présente dans le contexte.\n"
                    "N’intègre pas de ressources supplémentaires extérieures au département Scolarité.\n\n"
                    "**Gestion des Ressources :**\n"
                    "La section « 📚 Pour Aller Plus Loin » doit apparaître **uniquement si des ressources pertinentes sont disponibles** dans le contexte du département Scolarité.\n"
                    "Si aucune ressource n’est pertinente, **n’inclus pas cette section**.\n\n"
                    "**Important :**\n"
                    "Ne réponds à aucune question qui ne concerne pas le département Scolarité. Ignore toute demande hors de ce périmètre.\n"
                    "Exemple :\n"
                    "Q : Qu’est-ce que PySpark ?\n"
                    "R : Je ne peux répondre qu’aux questions relatives au département Scolarité.\n"
                ) + prompt_text

        else:
            prompt_text = (
                f"Question : {user_query}\n"
                "Réponds que tu n'as pas d'informations pertinentes pour cette question."
            )

        llm_raw_response = self.ollama_api.chat_with_ollama(prompt_text)
        cleaned_llm_response = self.clean_llm_response(llm_raw_response)

        chat_id = FilterManager.save_chat_history(
            user_id=user_id,
            question=user_query,
            answer=cleaned_llm_response,
            departement_id=departement_id,
            filiere_id=filiere_id,
            profile_id=profile_id,
            db_path=self.SQLITE_DB_PATH
        )

        return cleaned_llm_response, chat_id

    # def generate_response(self, user_query,user_id,profile_id, departement_id, filiere_id):
    #     # Appelle votre méthode pour trouver le contexte pertinent
    #     context_chunks = self.find_relevant_context(
    #         user_query, departement_id, filiere_id, top_k=3, similarity_threshold=0.55
    #     )

    #     prompt_text = "" # Initialise la variable pour le texte de l'invite

    #     if context_chunks:  # Si context_chunks n'est pas None et n'est pas une liste vide
    #         context_text_joined = "\n".join(context_chunks)
    #         #print(context_chunks)
    #         prompt_text = (
    #             f"Contexte :\n{context_text_joined}\n\n"
    #             f"Question : {user_query}\n"
    #                 """
    #                 vous êtes un assistant pédagogique. Réponds uniquement à partir du contexte fourni ci-dessus, sans ajouter, inférer ni reformuler d’informations extérieures.
    #                 Le cadre est académique : adopte un ton engageant et motivant pour l’étudiant, tout en restant clair, précis et inspirant.
    #                 Fournis une explication concise, sans introduction, justification ou répétition superflue.
    #                 Supprime toute balise <...> dans la réponse.
    #                 Exprime-toi uniquement en français.
    #                 Structure la réponse selon la charte suivante :

    #                 ********************
    #                 Réponse :
    #                 [Une phrase claire, précise et inspirante, directement issue du contexte.]
    #                 ********************

    #                 Ressources supplémentaires (si disponibles) :
    #                 - [Titre de la ressource 1] : [URL]
    #                 - [Titre de la ressource 2] : [URL]
    #                 ********************

    #                 N’affiche la section « Ressources supplémentaires » que si des ressources pertinentes sont disponibles.
    #                 Ne fournis jamais d’informations non présentes dans le contexte.

    #                 *********************
    #                 Si l'etudiant demande un QCM procède à ce qui suit : En te basant sur ce contexte extrait des documents de cours,
    #                 génère un QCM lié à la question suivante.

    #                 Contexte : 
    #                 {context_chunks}

    #                 Question : {user_query}

    #                 Génère une liste des questions QCM avec 4 propositions selon le nombre demandé par l'étudiant mais ne pas dépasser 10 au maximum, indique clairement la bonne réponse.

    #                 Format :

    #                 Question : [ta question]
    #                 1) choix A
    #                 2) choix B
    #                 3) choix C
    #                 4) choix D

    #                 Réponse correcte : [numéro ou texte]
    #                 """
    #         )
    #     else:
    #         # Ceci est l'invite de votre bloc 'else' original
    #         prompt_text = (
    #             f"Question : {user_query}\n"
    #             "Si la question est hors le cadre académique, répond par : je n'ai pas la capacité de répondre à votre question.\n\nRéponse :"
    #         )
        
    #     llm_raw_response = self.ollama_api.chat_with_ollama(prompt_text)
    #     cleaned_llm_response = self.clean_llm_response(llm_raw_response)

    #     FilterManager.save_chat_history(
    #         user_id=user_id, question=user_query, answer=cleaned_llm_response,
    #         departement_id=departement_id, filiere_id=filiere_id, profile_id=profile_id
    #     )
    #     return cleaned_llm_response

    def simulate_typing(self, text, delay=0.009):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def format_response(self, response):
        formatted_response = ""
        for char in response:
            if char.isdigit():
                formatted_response += Fore.BLUE + char + Style.RESET_ALL
            elif char == '`':
                formatted_response += Fore.GREEN + char + Style.RESET_ALL
            else:
                formatted_response += char
        return formatted_response

    def display_welcome_message(self):
        welcome_message = Fore.GREEN + "Chatbot: Bonjour ! Tapez 'exit' pour quitter." + Style.RESET_ALL
        self.simulate_typing(welcome_message)

    def display_exit_message(self):
        exit_message = Fore.RED + "Chatbot: Au revoir ! À bientôt !" + Style.RESET_ALL
        self.simulate_typing(exit_message)

    def chat(self, departement_id, filiere_id, module_id, activite_id, profile_id, user_id):
        self.display_welcome_message()
        while True:
            user_input = input("\n" + Fore.YELLOW + "Vous : " + Style.RESET_ALL)
            if user_input.lower() == "exit":
                self.display_exit_message()
                break
            try:
                response = self.generate_response(user_input, departement_id, filiere_id, module_id, activite_id, profile_id, user_id)
                formatted_response = self.format_response(response)
                self.simulate_typing(Fore.CYAN + f"Chatbot : {formatted_response}" + Style.RESET_ALL)
            except Exception as e:
                self.simulate_typing(Fore.RED + f"Chatbot : Désolé, une erreur s'est produite : {str(e)}" + Style.RESET_ALL)