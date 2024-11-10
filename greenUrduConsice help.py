import os
import pandas as pd
import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
from googletrans import Translator  # Import Translator for Google Translate

# Initialize the Translator object for Google Translate
translator = Translator()

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
GROQ_API_KEY = "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"  # Replace with your API Key
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Check if this is the correct URL

# Streamlit UI for the chatbot
st.markdown("""<style>
body {
    background-color: #f0f8ff;
    font-family: 'Arial', sans-serif;
}
.stButton button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    cursor: pointer;
    border-radius: 12px;
}
.stButton button:hover {
    background-color: #45a049;
}
.stTextInput input {
    border-radius: 10px;
    padding: 10px;
    border: 2px solid #4CAF50;
    width: 100%;
}
h1 {
    color: #4CAF50;
}
h2 {
    color: #4CAF50;
}
p {
    color: #333333;
}
</style>""", unsafe_allow_html=True)

# Greeting and initial introduction
st.title("DiscoverPak - Virtual Pakistan Travel Guide")
st.subheader("Your friendly virtual tour guide with 40 years of expertise in Pakistan's travel spots.")
st.write("Welcome! You can ask me about famous places, weather, events, or other travel-related topics in Pakistan.")

# Help dropdown with detailed features
with st.expander("Help", expanded=False):
    st.write("### Welcome to DiscoverPak!")
    st.write("This chatbot can assist you with the following features:")
    st.write("1. **Travel Information:** Get detailed information about famous travel destinations.")
    st.write("2. **Directions:** Guidance to reach various locations with travel tips.")
    st.write("3. **Weather Updates:** Current weather information for regions.")
    st.write("4. **Local Events:** Information on upcoming events and activities.")
    st.write("5. **Travel Tips:** Advice on safety, cultural etiquette, and more.")
    st.write("6. **Feedback and Queries:** Share your feedback or ask additional questions.")

# Text input for the user query
user_input = st.text_input("Type your question here", key="query")

# Button to submit the query and handle response
if st.button("Submit Query") or user_input:
    if user_input:
        try:
            # Request payload for the Groq API
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            payload = {
                "messages": [{"role": "user", "content": user_input}],
                "model": "llama3-8b-8192"
            }

            # Make the API call directly with requests
            response = requests.post(GROQ_API_URL, headers=headers, json=payload)

            # Check for 404 and log the error
            if response.status_code != 200:
                st.error(f"Error: {response.status_code}, {response.text}")
            
            response.raise_for_status()  # Raise error if status is not 200
            
            # Parse the API response
            response_json = response.json()
            if 'choices' in response_json and len(response_json['choices']) > 0:
                response_text = response_json['choices'][0]['message']['content']
                st.write("Chatbot response (DiscoverPak):")
                st.write(response_text)

                # Translate the response text into Urdu
                translated_text = translator.translate(response_text, src='en', dest='ur').text
                st.write("Chatbot response (in Urdu - DiscoverPak):")
                st.write(translated_text)

            else:
                st.error("Unexpected API response format. Please check the response structure.")
        except requests.exceptions.RequestException:
            # Fallback to offline mode response
            response_text = get_offline_response(user_input)
            st.write(response_text)

            # Translate the offline response into Urdu
            translated_text = translator.translate(response_text, src='en', dest='ur').text
            st.write("Offline response (in Urdu - DiscoverPak):")
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
st.write("Thank you for using DiscoverPak - Your Travel Assistant!")
feedback = st.text_input("Please provide your feedback here:")
if st.button("Submit Feedback"):
    st.write("Thank you for your feedback!")
