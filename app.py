import streamlit as st
import numpy as np
import librosa
from keras.models import load_model

# Load model
model = load_model('crime_detector.h5')

# Class labels
classes = ['air_conditioner', 'car_horn', 'children_playing', 'dog_bark', 'drilling',
           'engine_idling', 'gun_shot', 'jackhammer', 'siren', 'street_music']

# Feature extraction function
def extract_features(file):
    audio, sample_rate = librosa.load(file, res_type='kaiser_fast')
    mels = np.mean(librosa.feature.melspectrogram(y=audio, sr=sample_rate).T, axis=0)
    return mels.reshape(1, 128)

# Streamlit UI
st.title("Gunshot Audio Classifier")

uploaded_file = st.file_uploader("Upload an audio file (.wav)", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    try:
        features = extract_features(uploaded_file)
        prediction = model.predict(features)
        class_id = np.argmax(prediction)
        predicted_class = classes[class_id]

        st.success(f"**Predicted Sound:** {predicted_class}")
    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")
