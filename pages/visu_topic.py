import pandas as pd
import streamlit as st
import requests
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

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

    # Utilisation du style Seaborn pour améliorer l'esthétique
    sns.set(style="whitegrid")

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=daily_success_rate.index, y=daily_success_rate['success'], ax=ax, color='royalblue', marker='o', linewidth=2.5)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('% de Prédictions Correctes', fontsize=12)
    ax.set_title('Pourcentage de Réussite des Prédictions par Jour', fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='x', rotation=45)

    st.pyplot(fig)

# Fonction pour générer le graphique des succès par topic
def plot_topic_success_rate(df):
    # Création de la colonne 'success' qui représente le succès des prédictions
    df['success'] = (df['predicted_topic'] == df['real_topic']).astype(int)

    # Calcul du % de prédictions correctes par topic
    success_by_topic = df.groupby('real_topic').agg({'success': 'mean'}) * 100

    # Création du graphique avec Seaborn pour l'esthétique
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=success_by_topic.index, y=success_by_topic['success'], ax=ax, palette='Set2')

    ax.set_xlabel('Topic', fontsize=12)
    ax.set_ylabel('% de Prédictions Correctes', fontsize=12)
    ax.set_title('Pourcentage de Réussite des Prédictions par Topic', fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='x', rotation=45)

    # Ajouter les labels pour chaque barre
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f%%', label_type='edge')

    st.pyplot(fig)

# Streamlit app
st.title("📈 Suivi des Prédictions des Topics")

# Charger les données des topics
df_topics = get_topic_data()

if df_topics is not None:
    # Afficher le graphique des prédictions correctes par jour
    st.write("Voici le graphique montrant le pourcentage de prédictions correctes par jour.")
    plot_daily_success_rate(df_topics)

    # Afficher le graphique des prédictions correctes par topic
    st.write("Voici le graphique montrant le pourcentage de prédictions correctes par topic.")
    plot_topic_success_rate(df_topics)
