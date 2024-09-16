import streamlit as st
st.set_page_config(
    page_title="Natural Language Processing",
    page_icon=":speaking_head_in_silhouette::",
    layout="wide"
)

# Charger le fichier CSS pour le style
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("css/style.css")

# Introduction
st.markdown("""
    <div style='text-align: center;'>
        <h1>  Topic Modeling & Analyse de Sentiment</h1>
        <p>Ce projet offre trois fonctionnalités principales basées sur le traitement du langage naturel :</p>
    </div>
""", unsafe_allow_html=True)

# Définir les colonnes pour les sections
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-box">
            <h2>💌 Analyse de sentiment</h2>
            <p>Analysez les émotions et opinions exprimées dans un texte, qu'elles soient positives, négatives ou neutres.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-box">
            <h2>📓 Topic Modeling</h2>
            <p>Identifiez les sujets principaux au sein d'un corpus de documents en utilisant des techniques comme LDA (Latent Dirichlet Allocation).</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-box">
            <h2>📋 Monitoring</h2>
            <p>Suivez les performances des modèles avec des statistiques en temps réel et visualisez les résultats des analyses.</p>
        </div>
    """, unsafe_allow_html=True)
