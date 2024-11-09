# Install necessary libraries with map
!pip install --upgrade httpx
!pip install pandas streamlit requests googletrans==4.0.0-rc1 folium streamlit-folium



import os
import pandas as pd
import streamlit as st
import requests
from googletrans import Translator
import folium
from streamlit_folium import folium_static

# Load data from Excel file for offline mode
data = pd.read_excel("/content/pak.xlsx")

# Simulated offline response using the Excel data
def get_offline_response(query):
    # Search the Excel data for the best response
    for _, row in data.iterrows():
        if query.lower() in str(row['Description']).lower():
            return f"Offline mode: {row['Description']}"
    return "Offline mode: Information not available for your query."

# Groq API settings with corrected endpoint URL
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Initialize the Translator object for Google Translate
translator = Translator()

# Streamlit UI for the chatbot
st.title("Virtual Pakistan Travel Guide")
st.subheader("Your friendly virtual tour guide with 40 years of expertise in Pakistan's travel spots.")

# Greeting and initial introduction
st.write("Welcome! You can ask me about famous places, weather, events, or other travel-related topics in Pakistan.")

# Help dropdown with detailed features
with st.expander("Help", expanded=False):
    st.write("### Welcome to the Virtual Pakistan Travel Guide!")
    st.write("This chatbot can assist you with the following features:")
    st.write("1. **Travel Information:**")
    st.write("   - Get detailed information about famous travel destinations in Pakistan, including history, culture, and attractions.")
    st.write("2. **Directions:**")
    st.write("   - Receive guidance on how to reach various locations, including public transport options and travel tips.")
    st.write("3. **Language Support:**")
    st.write("   - Get responses in Urdu for better understanding and accessibility.")
    st.write("4. **Weather Updates:**")
    st.write("   - Inquire about current weather conditions in different regions of Pakistan.")
    st.write("5. **Local Events:**")
    st.write("   - Find out about upcoming events, festivals, and activities happening in various cities.")
    st.write("6. **Travel Tips:**")
    st.write("   - Get useful travel tips, including safety advice, cultural etiquette, and packing suggestions.")
    st.write("7. **Feedback and Queries:**")
    st.write("   - Share your feedback or ask any additional questions you might have.")
    st.write("### How to Use:")
    st.write("Simply type your question in the input box and click 'Submit Query' to receive assistance.")

# Text input for the user query
user_input = st.text_input("Type your question here")

# Button to submit the query and handle response
if st.button("Submit Query"):
    if user_input:
        # Check internet connection and switch to offline mode if unavailable
        try:
            # Request payload for the Groq API
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            payload = {
                "messages": [{"role": "user", "content": user_input}],
                "model": "llama3-8b-8192"
            }

            # Make the API call directly with requests
            response = requests.post(GROQ_API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx

            # Parse the API response
            response_json = response.json()
            if 'choices' in response_json and len(response_json['choices']) > 0:
                response_text = response_json['choices'][0]['message']['content']
                st.write("Chatbot response (in English):")
                st.write(response_text)

                # Translate the response text into Urdu
                translated_text = translator.translate(response_text, src='en', dest='ur').text
                st.write("Chatbot response (in Urdu):")
                st.write(translated_text)
            else:
                st.error("Unexpected API response format. Please check the response structure.")

        except requests.exceptions.RequestException:
            # Fallback to offline mode response
            response_text = get_offline_response(user_input)
            st.write(response_text)

            # Translate the offline response into Urdu
            translated_text = translator.translate(response_text, src='en', dest='ur').text
            st.write("Offline response (in Urdu):")
            st.write(translated_text)

# Map feature
st.subheader("Explore Tourist Locations on the Map")
map = folium.Map(location=[30.3753, 69.3451], zoom_start=5)  # Centered on Pakistan

# Add some tourist locations (latitude, longitude, name)
tourist_locations = [
    {"name": "Lahore Fort", "coordinates": [31.5820, 74.3293]},
    {"name": "Badshahi Mosque", "coordinates": [31.5820, 74.3090]},
    {"name": "Karachi Beach", "coordinates": [24.8607, 67.0011]},
    {"name": "Hunza Valley", "coordinates": [36.2950, 74.6484]},
]

for location in tourist_locations:
    folium.Marker(
        location["coordinates"],
        popup=location["name"],
        icon=folium.Icon(color='blue')
    ).add_to(map)

# Display the map in the Streamlit app
folium_static(map)

# Conclusion and feedback collection
st.write("Thank you for using the Pakistan Travel Assistant!")
feedback = st.text_input("Please provide your feedback here:")
if st.button("Submit Feedback"):
    st.write("Thank you for your feedback!")
