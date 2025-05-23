# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vLkOr_ZwPpIlu94PyaW_FLB4J4eVNokt
"""

from flask import Flask, request, render_template_string
import pandas as pd
import requests

app = Flask(__name__)

# Load cleaned CSV
df = pd.read_csv("cleaned_players.csv")
df['name'] = df['name'].str.lower()
df['club'] = df['club'].str.lower()

# API-Football Config
API_KEY = "ddb5ce1259efc7637ec9102b8c508108"
API_HOST = "v3.football.api-sports.io"

def get_premier_league_standings():
    url = "https://v3.football.api-sports.io/standings?league=39&season=2023"
    headers = {
        "x-rapidapi-host": API_HOST,
        "x-rapidapi-key": API_KEY
    }
    response = requests.get(url, headers=headers)
    try:
        data = response.json()
        standings = data['response'][0]['league']['standings'][0]
        top_3 = [(t['team']['name'], t['points']) for t in standings[:3]]
        return "\n".join([f"{name} ({pts} pts)" for name, pts in top_3])
    except:
        return "Error fetching standings."

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    if request.method == "POST":
        msg = request.form.get("message", "").lower()

        if "standings" in msg:
            reply = get_premier_league_standings()
        elif "goal" in msg:
            for name in df['name']:
                if name in msg:
                    g = int(df[df['name'] == name]['goals'].values[0])
                    reply = f"{name.title()} scored {g} goals."
                    break
        elif "assist" in msg:
            for name in df['name']:
                if name in msg:
                    a = int(df[df['name'] == name]['assists'].values[0])
                    reply = f"{name.title()} had {a} assists."
                    break
        elif "appearance" in msg:
            for name in df['name']:
                if name in msg:
                    apps = int(df[df['name'] == name]['appearances'].values[0])
                    reply = f"{name.title()} made {apps} appearances."
                    break
        if not reply:
            reply = "Sorry, I couldn't find the answer."

    return render_template_string("""
    <html><body>
    <h1>Premier League Chatbot</h1>
    <form method="post">
        <input name="message" placeholder="Ask a question..." size="50"/>
        <input type="submit" value="Ask"/>
    </form>
    {% if reply %}
    <p><strong>Response:</strong> {{ reply }}</p>
    {% endif %}
    </body></html>
    """, reply=reply)