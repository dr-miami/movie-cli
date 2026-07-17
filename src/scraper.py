import os
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://67movies.net"
TMDB_API = "https://api.themoviedb.org/3"
TMDB_IMG = "https://image.tmdb.org/t/p/w200"

# Search for a movie or TV show using the TMDB API
def search_media(query, media_type):
    endpoint = "movie" if media_type == "movie" else "tv"
    params = {
        "api_key": API_KEY,
        "query": query,
        "language": "en-US",
        "page": 1
    }
    resp = requests.get(f"{TMDB_API}/search/{endpoint}", params=params)
    resp.raise_for_status()
    results = []
    for item in resp.json().get("results", []):
        title = item.get("title") if media_type == "movie" else item.get("name")
        year = (item.get("release_date") or item.get("first_air_date") or "")[:4]
        results.append({
            "id": item["id"],
            "title": title or "Unknown",
            "year": year,
            "poster": TMDB_IMG + item["poster_path"] if item.get("poster_path") else None
        })
    return results

# Fetch all seasons and episodes for a given TV show ID
def get_tv_episodes(tv_id):
    url = f"{TMDB_API}/tv/{tv_id}"
    params = {"api_key": API_KEY, "language": "en-US"}
    data = requests.get(url, params=params).json()
    ep_map = {}
    for season in data.get("seasons", []):
        sn = season.get("season_number")
        if sn is None:
            continue
        ep_map[sn] = {"name": season.get("name", f"Season {sn}"), "episodes": []}
    for sn in list(ep_map.keys()):
        season_url = f"{TMDB_API}/tv/{tv_id}/season/{sn}"
        params_s = {"api_key": API_KEY, "language": "en-US"}
        resp = requests.get(season_url, params=params_s)
        if resp.status_code == 200:
            for ep in resp.json().get("episodes", []):
                ep_map[sn]["episodes"].append({
                    "episode_number": ep.get("episode_number"),
                    "name": ep.get("name", f"Episode {ep.get('episode_number')}")
                })
    return ep_map

# Extract the embed iframe URL from the 67movies page
def get_embed_url(media_type, media_id, season=None, episode=None):
    if media_type == "movie":
        page_url = f"{BASE_URL}/watch/movie/{media_id}"
    else:
        page_url = f"{BASE_URL}/watch/tv/{media_id}/{season}/{episode}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(page_url, headers=headers)
    if resp.status_code != 200 and media_type == "tv":
        page_url = f"{BASE_URL}/watch/tv/{media_id}?s={season}&e={episode}"
        resp = requests.get(page_url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    iframe = soup.find("iframe")
    return iframe["src"] if iframe else None