import pandas as pd
import streamlit as st
import requests
from io import StringIO
import matplotlib.pyplot as plt

# Récupération des données via l'API pour les topics
def get_topic_data():
    url = "http://topicwebapp-g0g7hshfhugta5cy.francecentral-01.azurewebsites.net/export_data?table_name=monitoring_topic"
    response = requests.get(url)

    if response.status_code != 200:
        st.error("Erreur lors de la récupération des données.")
        return None

    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)

    # Conversion des dates au format datetime
    df['prediction_time'] = pd.to_datetime(df['prediction_time'])
    df['date'] = df['prediction_time'].dt.date  # Extraire uniquement la date
    return df

# Fonction pour générer le graphique des succès par jour
def plot_daily_success_rate(df):
    # Création de la colonne 'success' qui représente le succès des prédictions
    df['success'] = (df['predicted_topic'] == df['real_topic']).astype(int)

    # Calcul du % de prédictions correctes par jour
    daily_success_rate = df.groupby('date').agg({'success': 'mean'}) * 100

    # Création du graphique
    fig, ax = plt.subplots()
    daily_success_rate.plot(kind='line', ax=ax, color='blue', legend=False, marker='o')
    ax.set_xlabel('Date')
    ax.set_ylabel('% de prédictions correctes')
    ax.set_title('Pourcentage de réussite des prédictions par jour')

    for i in ax.containers:
        ax.bar_label(i, fmt='%.2f%%', label_type='edge')

    st.pyplot(fig)

# Fonction pour générer le graphique des succès par topic
def plot_topic_success_rate(df):
    # Création de la colonne 'success' qui représente le succès des prédictions
    df['success'] = (df['predicted_topic'] == df['real_topic']).astype(int)

    # Calcul du % de prédictions correctes par topic
    success_by_topic = df.groupby('real_topic').agg({'success': 'mean'}) * 100

    # Création du graphique
    fig, ax = plt.subplots()
    success_by_topic.plot(kind='bar', ax=ax, color='green', legend=False)
    ax.set_xlabel('Topic')
    ax.set_ylabel('% de prédictions correctes')
    ax.set_title('Pourcentage de réussite des prédictions par topic')

    for i in ax.containers:
        ax.bar_label(i, fmt='%.2f%%', label_type='edge')

    st.pyplot(fig)

# Streamlit app
st.title("Suivi des Prédictions des Topics")

# Charger les données des topics
df_topics = get_topic_data()

if df_topics is not None:
    # Afficher le graphique des prédictions correctes par jour
    st.write("Voici le graphique montrant le pourcentage de prédictions correctes par jour.")
    plot_daily_success_rate(df_topics)

    # Afficher le graphique des prédictions correctes par topic
    st.write("Voici le graphique montrant le pourcentage de prédictions correctes par topic.")
    plot_topic_success_rate(df_topics)
