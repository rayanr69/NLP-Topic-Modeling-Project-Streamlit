import pandas as pd
import streamlit as st
import requests
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

# Récupération des données via l'API pour les sentiments
def get_sentiment_data():
    url = "http://topicwebapp-g0g7hshfhugta5cy.francecentral-01.azurewebsites.net/export_data?table_name=monitoring_sentiment"
    response = requests.get(url)

    if response.status_code != 200:
        st.error("Erreur lors de la récupération des données.")
        return None

    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df

# Fonction pour générer les graphiques
def plot_sentiment_graphs(df):
    df['prediction_date'] = pd.to_datetime(df['prediction_date'])

    # Calcul du succès par ligne
    df['success'] = (df['prediction'] == df['real_sentiment']).astype(int)

    # Calcul du pourcentage de succès par jour
    df_daily = df.set_index('prediction_date').resample('D').agg({'success': 'mean'}) * 100

    # Utiliser un style Seaborn pour rendre les graphiques plus élégants
    sns.set(style="whitegrid")

    # Graphique pour le succès par jour
    fig_daily, ax_daily = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=df_daily.index, y=df_daily['success'], ax=ax_daily, color='royalblue', linewidth=2.5)
    ax_daily.set_xlabel('Date', fontsize=12)
    ax_daily.set_ylabel('% de Prédictions Correctes', fontsize=12)
    ax_daily.set_title('Suivi des Prédictions de Sentiments par Jour', fontsize=14, fontweight='bold')
    ax_daily.grid(True, linestyle='--', alpha=0.6)
    ax_daily.tick_params(axis='x', rotation=45)
    st.pyplot(fig_daily)

    # Calcul du % de prédictions réussies pour les sentiments positifs et négatifs
    df_positive = df[df['real_sentiment'] == 'positive'].set_index('prediction_date').resample('D').agg({'success': 'mean'}) * 100
    df_negative = df[df['real_sentiment'] == 'negative'].set_index('prediction_date').resample('D').agg({'success': 'mean'}) * 100

    # Graphique pour les sentiments positifs
    fig_positive, ax_positive = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=df_positive.index, y=df_positive['success'], ax=ax_positive, color='green', linewidth=2.5)
    ax_positive.set_xlabel('Date', fontsize=12)
    ax_positive.set_ylabel('% de Prédictions Positives Correctes', fontsize=12)
    ax_positive.set_title('Pourcentage de Réussite des Prédictions pour les Sentiments Positifs', fontsize=14, fontweight='bold')
    ax_positive.grid(True, linestyle='--', alpha=0.6)
    ax_positive.tick_params(axis='x', rotation=45)
    st.pyplot(fig_positive)

    # Graphique pour les sentiments négatifs
    fig_negative, ax_negative = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=df_negative.index, y=df_negative['success'], ax=ax_negative, color='red', linewidth=2.5)
    ax_negative.set_xlabel('Date', fontsize=12)
    ax_negative.set_ylabel('% de Prédictions Négatives Correctes', fontsize=12)
    ax_negative.set_title('Pourcentage de Réussite des Prédictions pour les Sentiments Négatifs', fontsize=14, fontweight='bold')
    ax_negative.grid(True, linestyle='--', alpha=0.6)
    ax_negative.tick_params(axis='x', rotation=45)
    st.pyplot(fig_negative)

# Streamlit app
st.title("📈 Suivi des Prédictions des Sentiments")

# Charger et afficher les graphiques
df_sentiments = get_sentiment_data()
if df_sentiments is not None:
    st.write("Voici les graphiques montrant le pourcentage de prédictions correctes par jour et pour chaque type de sentiment (positif et négatif).")
    plot_sentiment_graphs(df_sentiments)
