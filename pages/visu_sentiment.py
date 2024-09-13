import pandas as pd
import streamlit as st
import requests
from io import StringIO
import matplotlib.pyplot as plt

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

    fig_daily, ax_daily = plt.subplots()
    ax_daily.plot(df_daily.index, df_daily['success'], label='% de prédictions correctes par jour', color='blue')
    ax_daily.set_xlabel('Date')
    ax_daily.set_ylabel('% de prédictions correctes')
    ax_daily.set_title('Suivi des prédictions de sentiments par jour')
    ax_daily.legend()
    st.pyplot(fig_daily)

    # Calcul du % de prédictions réussies pour les sentiments positifs et négatifs
    df_positive = df[df['real_sentiment'] == 'positive'].set_index('prediction_date').resample('D').agg({'success': 'mean'}) * 100
    df_negative = df[df['real_sentiment'] == 'negative'].set_index('prediction_date').resample('D').agg({'success': 'mean'}) * 100

    # Visualisation des % de réussite pour les sentiments positifs
    fig_positive, ax_positive = plt.subplots()
    ax_positive.plot(df_positive.index, df_positive['success'], label='% de prédictions positives correctes', color='green')
    ax_positive.set_xlabel('Date')
    ax_positive.set_ylabel('% de prédictions positives correctes')
    ax_positive.set_title('Pourcentage de réussite des prédictions pour les sentiments positifs')
    ax_positive.legend()
    st.pyplot(fig_positive)

    # Visualisation des % de réussite pour les sentiments négatifs
    fig_negative, ax_negative = plt.subplots()
    ax_negative.plot(df_negative.index, df_negative['success'], label='% de prédictions négatives correctes', color='red')
    ax_negative.set_xlabel('Date')
    ax_negative.set_ylabel('% de prédictions négatives correctes')
    ax_negative.set_title('Pourcentage de réussite des prédictions pour les sentiments négatifs')
    ax_negative.legend()
    st.pyplot(fig_negative)

# Streamlit app
st.title("Suivi des Prédictions des Sentiments")

# Charger et afficher les graphiques
df_sentiments = get_sentiment_data()
if df_sentiments is not None:
    st.write("Voici les graphiques montrant le pourcentage de prédictions correctes par jour et pour chaque type de sentiment (positif et négatif).")
    plot_sentiment_graphs(df_sentiments)
