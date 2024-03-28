import streamlit as st
import pandas as pd
import os
import io
import wave
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import time

# Définition des langues prises en charge
LANGUAGES = ["Arabe", "Francais", "Anglais", "Japonais", "Allemand"]

# Charger les bases de données des livres
books_english_df = pd.read_excel("C:/Users/pc/Documents/DEGILA_Elysee/Cours UEMF 2/Learning Non_supervise/TPs/Analyse_Pollution.xlsx")  # Exemple de fichier Excel pour les livres anglais
books_spanish_df = pd.read_excel("C:/Users/pc/Documents/DEGILA_Elysee/Cours UEMF 2/Learning Non_supervise/TPs/Analyse_Pollution.xlsx")  # Exemple de fichier Excel pour les livres espagnols
books_french_df = pd.read_excel("C:/Users/pc/Documents/DEGILA_Elysee/Cours UEMF 2/Learning Non_supervise/TPs/Analyse_Pollution.xlsx")  # Exemple de fichier Excel pour les livres français

# Fonction pour enregistrer la voix par microphone
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        info_message = st.info("Parlez maintenant...")
        audio_data = recognizer.listen(source)
        info_message.empty()  # Supprimer le message d'information après enregistrement
    # Écrire les données audio dans un fichier WAV temporaire
    with io.BytesIO() as wav_buffer:
        with wave.open(wav_buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(44100)  # Sample rate
            wav_file.writeframes(audio_data.frame_data)
        wav_bytes = wav_buffer.getvalue()

    # Afficher les données audio avec st.audio()
    st.audio(wav_bytes, format="audio/wav")
    success_message = st.empty()
    success_message.success("Enregistrement vocal terminé.")
    time.sleep(2)  # Temps d'affichage du message en secondes
    success_message.empty()
    return wav_bytes

# Fonction pour reconnaître la langue à partir d'un fichier audio
def recognize_language_from_audio(audio_data):
    # Ici, vous devriez implémenter votre propre fonction pour reconnaître la langue à partir des données audio
    # Pour l'exemple, je vais simplement retourner une langue aléatoire de la liste des langues prises en charge
    return LANGUAGES[1]


st.title("Reconnaissance de la Langue & Lecture")

# Afficher les images représentant chaque base de données de livres avec des boutons désactivés
st.write("Accédez à la base de données de livres :")

# Boutons pour accéder aux différentes bases de données de livres
col1, col2, col3 = st.columns(3)
with col1:
    st.image("C:/Users/pc/Documents/DEGILA_Elysee/Cours UEMF 2/Synthese_Parole/ecrin.png", caption="Livres Anglais")
    button_english = st.button("Accéder aux livres Anglais",key='1',  disabled=False)

with col2:
    st.image("C:/Users/pc/Documents/DEGILA_Elysee/Cours UEMF 2/Synthese_Parole/ecrin.png", caption="Livres Espagnols")
    button_spanish = st.button("Accéder aux livres Espagnols", key='2', disabled=False)

with col3:
    st.image("C:/Users/pc/Documents/DEGILA_Elysee/Cours UEMF 2/Synthese_Parole/ecrin.png", caption="Livres Francais")
    button_french = st.button("Accéder aux livres Francais", key='3', disabled=False)


st.sidebar.title("Enregistrement vocal")

if st.sidebar.button("Commencer l'enregistrement vocal"):
    data = record_audio()
    recognized_language = recognize_language_from_audio(data)
    if recognized_language == "Francais":
        st.write(recognized_language)
        if button_french:
            st.subheader("Livres Francais")
            st.dataframe(books_french_df)  # Afficher le DataFrame correspondant aux livres français
            # Sélectionner un livre dans la DataFrame affichée
            selected_book_id = st.selectbox("Sélectionnez un livre :", books_french_df["County"])

            # Obtenir le nom du livre sélectionné
            selected_book_name = books_french_df.loc[books_french_df["County"] == selected_book_id, "State"].iloc[0]

            # Afficher le contenu du livre sélectionné
            if selected_book_id:
                if st.button(f"Lire le livre '{selected_book_name}'"):
                    st.subheader(f"Contenu du livre '{selected_book_name}' :")
                    # Obtenir le chemin du fichier du livre
                    script_dir = os.path.dirname(__file__)  # Récupérer le répertoire du script Python en cours d'exécution
                    book_file_path = os.path.join(script_dir, f"{selected_book_name}.txt")  # Chemin absolu du fichier du livre
                    try:
                        # Ouvrir et afficher le contenu du livre
                        with open(book_file_path, "r") as book_file:
                            book_content = book_file.read()
                            st.write(book_content)
                    except FileNotFoundError:
                        st.error(f"Le fichier du livre '{selected_book_name}' n'a pas été trouvé.")
    else:
        st.write("Aucune langue reconnue.")

#recognized_language = recognize_language_from_audio(data)
#st.write(data)