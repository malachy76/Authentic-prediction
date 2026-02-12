from dotenv import load_dotenv
import os

# loads variables from .env file
load_dotenv()  
API_KEY = os.getenv("API_KEY")

import requests
import streamlit as st
import os

# Load API key from environment variable
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.football-data.org/v4"
headers = {"X-Auth-Token": API_KEY}

def check_api_key():
    """Test if API key works by fetching Premier League info."""
    url = f"{BASE_URL}/competitions/PL"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return f"✅ API key works! Competition name: {data.get('name')}"
    else:
        return f"❌ API key failed. Status code: {response.status_code} | Response: {response.text}"

# Streamlit UI
st.title("⚽ European League Prediction App")

st.write("This app highlights matches where:")
st.write("- A team has **5 consecutive wins**")
st.write("- That team has **odds ≤ 1.50** in their next fixture")

# 🔑 Add API Key Check Button
if st.button("Check API Key"):
    result = check_api_key()
    st.info(result)

import requests
import streamlit as st
import os

# Load API key from environment variable
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.football-data.org/v4"
headers = {"X-Auth-Token": API_KEY}

def has_five_wins(team_id):
    """Check if a team has won its last 5 matches."""
    url = f"{BASE_URL}/teams/{team_id}/matches?status=FINISHED&limit=5"
    response = requests.get(url, headers=headers).json()
    matches = response.get('matches', [])
    if len(matches) < 5:
        return False
    return all(
        (m['score']['winner'] == "HOME_TEAM" and m['homeTeam']['id'] == team_id) or
        (m['score']['winner'] == "AWAY_TEAM" and m['awayTeam']['id'] == team_id)
        for m in matches
    )

def get_upcoming_matches(league_id):
    """Fetch upcoming matches for a league."""
    url = f"{BASE_URL}/competitions/{league_id}/matches?status=SCHEDULED"
    response = requests.get(url, headers=headers).json()
    return response.get('matches', [])

# Streamlit UI
st.title("⚽ European League Prediction App")

st.write("This app highlights matches where:")
st.write("- A team has **5 consecutive wins**")
st.write("- That team has **odds ≤ 1.50** in their next fixture")

leagues = ["PL", "ELC", "BL1", "BL2", "PD", "SD"]  # Example league codes
flagged_matches = []

for league in leagues:
    matches = get_upcoming_matches(league)
    for match in matches:
        home_id = match['homeTeam']['id']
        away_id = match['awayTeam']['id']

        # Check home team streak + odds
        if has_five_wins(home_id):
            odds = match.get('odds', {}).get('homeWin', None)
            if odds and odds <= 1.50:
                flagged_matches.append((match['homeTeam']['name'], match['awayTeam']['name'], odds, league))

        # Check away team streak + odds
        if has_five_wins(away_id):
            odds = match.get('odds', {}).get('awayWin', None)
            if odds and odds <= 1.50:
                flagged_matches.append((match['awayTeam']['name'], match['homeTeam']['name'], odds, league))

st.subheader("Predicted Matches")
if flagged_matches:
    for team, opponent, odds, league in flagged_matches:
        st.write(f"**{team}** vs {opponent} | Odds: {odds} | League: {league}")
else:
    st.write("No qualifying matches found yet.")
