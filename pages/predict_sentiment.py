import streamlit as st
import requests

# Configuration de la page
st.set_page_config(page_title="Analyse de Sentiment", page_icon="🔍", layout="wide")

# Titre de l'application
st.title("🔍 Analyse de Sentiment - Prédiction")

# Introduction
st.markdown("""
Bienvenue dans l'outil d'analyse de sentiment ! Utilisez cette application pour tester la connexion à l'API et analyser le sentiment d'un texte en prédictant s'il est **positif** ou **négatif**.
""")

# Section pour tester la connexion avec l'API
st.header("🔗 Tester la connexion à l'API")

# Utilisation d'une colonne pour une disposition plus harmonieuse
col1, col2 = st.columns([1, 4])

with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Connected_world_icon.svg/1024px-Connected_world_icon.svg.png", width=80)

with col2:
    # Bouton pour tester la connexion à l'API
    if st.button("Tester la connexion API"):
        try:
            # URL de l'API pour vérifier son statut
            status_url = "https://topicwebapp-g0g7hshfhugta5cy.francecentral-01.azurewebsites.net/status"
            response = requests.get(status_url)

            # Afficher la réponse
            if response.status_code == 200:
                st.success("L'API est en ligne et opérationnelle ! 🚀")
            else:
                st.error(f"Erreur de connexion à l'API : {response.status_code}")
        except Exception as e:
            st.error(f"Erreur lors de la tentative de connexion : {e}")

# Séparateur visuel
st.markdown("---")

# Section d'analyse de sentiment
st.header("📝 Analyse de Sentiment")

# Explication du processus
st.markdown("Entrez un texte dans la zone ci-dessous pour obtenir une **prédiction** sur le sentiment (positif ou négatif) de ce texte.")

# Zone de texte pour entrer le texte utilisateur
user_input = st.text_area("💬 Entrez le texte pour lequel vous souhaitez prédire les sentiments :", height=150)

# Bouton pour valider et obtenir la prédiction
if st.button("Valider"):
    if user_input.strip():
        try:
            # URL de l'API pour faire la prédiction
            predict_url = "https://topicwebapp-g0g7hshfhugta5cy.francecentral-01.azurewebsites.net/predict_s"

            # Données à envoyer à l'API
            data = {"text": user_input}

            # Requête POST pour obtenir les prédictions
            response = requests.post(predict_url, json=data)

            # Vérifier la réponse de l'API
            if response.status_code == 200:
                # Extraire la réponse de la prédiction
                prediction = response.json()

                # Afficher le résultat avec style
                st.subheader("🎯 Résultat de la prédiction")
                sentiment = prediction.get("sentiment", "Non disponible")
                score = prediction.get("score", "Non disponible")

                # Affichage du résultat avec couleur selon le sentiment
                if sentiment == "positif":
                    st.success(f"Sentiment : **Positif** (Score : {score:.2f})")
                elif sentiment == "négatif":
                    st.error(f"Sentiment : **Négatif** (Score : {score:.2f})")
                else:
                    st.warning(f"Sentiment : {sentiment}")
            else:
                st.error(f"Erreur lors de la prédiction : {response.status_code}")
        except Exception as e:
            st.error(f"Erreur lors de l'envoi de la requête : {e}")
    else:
        st.warning("⚠️ Veuillez entrer un texte avant de valider.")

# Note de bas de page
st.markdown("""
---
*Cette application utilise un modèle de machine learning pour analyser les sentiments d'un texte via une API externe.*
""")
