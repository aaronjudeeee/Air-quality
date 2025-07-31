import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_KEY = 'your_api_key_here'

def get_aqi_data(city):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={city_lat}&lon={city_lon}&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

# Example city coordinates for Delhi
city = "Delhi"
city_lat = 28.6139
city_lon = 77.2090

st.title("🌫️ Real-Time Air Quality Dashboard")
st.write(f"Live AQI for: **{city}**")

data = get_aqi_data(city)
aqi = data['list'][0]['main']['aqi']
components = data['list'][0]['components']

# AQI Level
aqi_label = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
st.metric("Air Quality Index (AQI)", f"{aqi} - {aqi_label[aqi]}")

# Bar chart for pollutants
df = pd.DataFrame.from_dict(components, orient='index', columns=['Concentration (µg/m³)'])
st.bar_chart(df)
