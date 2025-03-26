from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Base URLs for the API
TRENDING_URL = "https://animeapi.skin/trending"
NEW_ANIME_URL = "https://animeapi.skin/new?page={}"
SEARCH_URL = "https://animeapi.skin/search?q={}"
EPISODES_URL = "https://animeapi.skin/episodes?title={}"
EMBED_BASE_URL = "https://2anime.xyz/embed/{}"

@app.route('/')
def home():
    # Fetch trending anime
    try:
        response = requests.get(TRENDING_URL)
        trending = response.json() if response.status_code == 200 else []
    except:
        trending = []
    
    # Fetch new anime (first page)
    try:
        response = requests.get(NEW_ANIME_URL.format(1))
        new_anime = response.json() if response.status_code == 200 else []
    except:
        new_anime = []
    
    return render_template('index.html', trending=trending, new_anime=new_anime)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    try:
        response = requests.get(SEARCH_URL.format(query))
        results = response.json() if response.status_code == 200 else []
    except:
        results = []
    
    return render_template('search_results.html', results=results, query=query)

@app.route('/anime/<title>')
def anime_episodes(title):
    try:
        response = requests.get(EPISODES_URL.format(title))
        episodes = response.json() if response.status_code == 200 else []
    except:
        episodes = []
    
    return render_template('episodes.html', episodes=episodes, title=title)

@app.route('/embed/<title>-episode-<int:episode>')
def embed(title, episode):
    embed_url = EMBED_BASE_URL.format(f"{title}-episode-{episode}")
    return render_template('embed.html', embed_url=embed_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
