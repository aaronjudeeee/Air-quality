import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="COVID-19 Tracker", layout="centered")
st.title("🦠 COVID-19 Real-Time Tracker")

# Fetch list of countries
@st.cache_data(ttl=3600)
def get_countries():
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    data = response.json()
    return sorted([country['country'] for country in data])

countries = get_countries()
countries.insert(0, "Global")

selected_country = st.selectbox("Select a country", countries)

# Fetch COVID stats
@st.cache_data(ttl=300)
def get_stats(country):
    if country == "Global":
        url = "https://disease.sh/v3/covid-19/all"
    else:
        url = f"https://disease.sh/v3/covid-19/countries/{country}"
    response = requests.get(url)
    return response.json()

# Fetch historical data for chart
@st.cache_data(ttl=300)
def get_historical(country):
    if country == "Global":
        url = "https://disease.sh/v3/covid-19/historical/all?lastdays=60"
    else:
        url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=60"
    response = requests.get(url)
    return response.json()

stats = get_stats(selected_country)

st.subheader(f"Current COVID-19 Stats - {selected_country}")
cols = st.columns(3)
cols[0].metric("Total Cases", f"{stats.get('cases', 'N/A'):,}")
cols[1].metric("Total Deaths", f"{stats.get('deaths', 'N/A'):,}")
cols[2].metric("Total Recovered", f"{stats.get('recovered', 'N/A'):,}")

historical = get_historical(selected_country)

# Prepare data for new cases chart
if selected_country == "Global":
    cases = historical.get("cases", {})
else:
    cases = historical.get("timeline", {}).get("cases", {})

if cases:
    df = pd.DataFrame(list(cases.items()), columns=["Date", "Cases"])
    df["Date"] = pd.to_datetime(df["Date"])
    df["New Cases"] = df["Cases"].diff().fillna(0)

    st.subheader("Daily New Cases (Last 60 days)")
    fig = px.bar(df, x="Date", y="New Cases", labels={"New Cases": "New Cases"}, height=400)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No historical data available for this location.")






