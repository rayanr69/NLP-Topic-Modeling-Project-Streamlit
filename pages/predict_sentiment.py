import streamlit as st
import requests  # Import manquant

# Titre de l'application
st.title("BONUS : Sentiment Analysis")

# Section pour tester la connexion avec l'API
st.header("Tester la connexion à l'API")

# Bouton pour tester si l'API est connectée
if st.button("Tester la connexion API"):
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

# Fonction de prédiction du sentiment

# Interface Streamlit
st.header("Analyse de Sentiment")
st.write("Entrez un texte ci-dessous pour savoir s'il est positif ou négatif.")

# Saisie du texte par l'utilisateur
user_input = st.text_area("Entrez le texte pour lequel vous souhaitez prédire les sentiments:")

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
                st.write(prediction)  # Afficher le résultat
            else:
                st.error(f"Erreur de prédiction: {response.status_code}")
        except Exception as e:
            st.error(f"Erreur lors de l'envoi de la requête: {e}")
    else:
        st.warning("Veuillez entrer un texte avant de valider.")
