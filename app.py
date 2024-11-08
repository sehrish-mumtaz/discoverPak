# Install necessary libraries (only needed in Google Colab or fresh environments)
!pip install SpeechRecognition gTTS openai groq whisper streamlit pandas



# Importing required libraries
import os
import pandas as pd
import openai
from groq import Groq
from gtts import gTTS
import whisper
import streamlit as st
import speech_recognition as sr
import tempfile

# Load the Whisper model
whisper_model = whisper.load_model("base")

# Initialize Groq API
groq_client = Groq(api_key="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")

# Load your local Excel data for tourist locations
tourist_data = pd.read_excel("/content/pak1.xlsx")

# Function to transcribe audio using Whisper model
def transcribe_audio(audio_file):
    result = whisper_model.transcribe(audio_file)
    return result["text"]

# Function to get response from Groq API
def get_groq_response(user_input):
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content

# Function to convert text to speech using gTTS
def text_to_speech(response_text):
    tts = gTTS(text=response_text, lang='en')
    audio_file = tempfile.NamedTemporaryFile(delete=False)
    tts.save(audio_file.name)
    return audio_file.name

# Streamlit UI Setup
st.title("DiscoverPak Travel Assistant")

# Greeting Message
st.subheader("Welcome to DiscoverPak! Ask me anything about traveling in Pakistan.")

# Streamlit components for text-based input
text_input = st.text_area("Ask me a question about traveling in Pakistan:")

# Function to handle both text and audio responses
def handle_input(user_input):
    if user_input:  # If the user has entered text
        st.write(f"You said: {user_input}")

        # Get response from Groq API
        response = get_groq_response(user_input)
        st.write(f"Bot's response: {response}")

        # Convert response to speech
        audio_path = text_to_speech(response)
        st.audio(audio_path, format='audio/mp3')

# Text input handling
if st.button("Submit"):
    if text_input:
        handle_input(text_input)
    else:
        st.write("Please enter a question.")

# Feedback collection section
st.subheader("Give Your Feedback!")
if st.button("Provide Feedback"):
    feedback = st.text_area("Please share your feedback:")
    if feedback:
        st.write("Thank you for your feedback!")
        # You can store the feedback in a file or database here (optional)

#1st code to run streamlit on google colab
!wget -q -O - ipv4.icanhazip.com

#2nd code to run streamlit on google colab
!streamlit run app.py & npx localtunnel --port 8501
