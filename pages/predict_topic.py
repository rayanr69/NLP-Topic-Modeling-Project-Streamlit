import streamlit as st
import requests
import pandas as pd
# Configuration de la mise en page
st.set_page_config(
    page_title="NLP Topic Modeling",
    page_icon="🧠",
    layout="wide"
)

# En-tête principal avec un titre stylisé
st.title("🧠 Prédiction Topic Modeling")

# Introduction
st.markdown("""
Bienvenue sur l'interface de déploiement du projet **NLP Topic Modeling**.
Utilisez cette application pour tester la connexion à l'API et prédire les thèmes d'un texte à l'aide de modèles de traitement du langage naturel (NLP).
""")

# Section pour tester la connexion avec l'API
st.header("🔌 Tester la connexion à l'API")

# Utilisation de colonnes pour une présentation plus fluide
col1, col2 = st.columns([2, 5])

with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Lightbulb_icon.svg/2048px-Lightbulb_icon.svg.png", width=100)

with col2:
    # Bouton pour tester la connexion à l'API
    if st.button("🔍 Tester la connexion API"):
        try:
            # URL de l'API pour vérifier son statut
            status_url = "https://topicwebapp-g0g7hshfhugta5cy.francecentral-01.azurewebsites.net/status"
            response = requests.get(status_url)

            # Afficher la réponse
            if response.status_code == 200:
                st.success("L'API est en ligne! 🚀")
            else:
                st.error(f"Erreur de connexion à l'API: {response.status_code}")
        except Exception as e:
            st.error(f"Erreur lors de la tentative de connexion: {e}")

# Séparation visuelle
st.markdown("---")

# Section pour faire une prédiction
st.header("📝 Faire une prédiction sur un texte")

# Explication supplémentaire
st.markdown("Entrez un texte dans la zone ci-dessous et obtenez une prédiction sur les topics probables.")

# Utilisation d'une zone de texte pour entrer le texte utilisateur
user_input = st.text_area("💬 Entrez le texte pour lequel vous souhaitez prédire les topics:", height=150)

# Bouton pour valider et envoyer la prédiction
if st.button("📊 Valider"):
    if user_input.strip():
        try:
            # URL de l'API pour faire la prédiction
            predict_url = "https://topicwebapp-g0g7hshfhugta5cy.francecentral-01.azurewebsites.net/predict"

            # Données à envoyer à l'API
            data = {"text": user_input}

            # Requête POST pour obtenir les prédictions
            response = requests.post(predict_url, json=data)

            # Vérifier la réponse de l'API
            if response.status_code == 200:
                # Extraire la distribution des topics de la réponse
                prediction = response.json()

                # Afficher les résultats sous forme de tableau
                st.write("### 📋 Distribution des Topics")
                topics = prediction.get("topic_distribution", [])
                if topics:
                    # Utiliser un tableau pour une meilleure présentation
                    df = pd.DataFrame(topics)
                    df.columns = ["Thème", "Probabilité"]
                    df["Probabilité"] = df["Probabilité"].apply(lambda x: f"{x:.2f}")
                    st.table(df)
                else:
                    st.warning("Aucune distribution de topics reçue.")
            else:
                st.error(f"Erreur de prédiction: {response.status_code}")
        except Exception as e:
            st.error(f"Erreur lors de l'envoi de la requête: {e}")
    else:
        st.warning("⚠️ Veuillez entrer un texte avant de valider.")

# Pied de page avec une note d'information
st.markdown("""
---
*Cette application utilise un modèle de NLP pour extraire les topics d'un texte donné. Elle se connecte à une API hébergée pour obtenir les prédictions.*
""")
