import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import json
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="VibeDJ 🎧🌀💿", page_icon="🎧", layout="centered")

# --- Title and Intro ---
st.title("🎧 VibeDJ")
st.subheader("🌀 A Playlist Generator That Feels Your Mood")
st.markdown("""
Welcome to **VibeDJ** – your AI-powered vibe curator.  
Tell me how you're feeling, and I’ll whip up a playlist that matches your soul.  
Sad breakup? Existential crisis? Gym grind? I’ve got a track for that. 💿  
""")

# --- Avatar ---
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://i.imgur.com/edwXSJa.png' width='200'/>
        <p><em>Your emotional DJ in the cloud ☁️🎶</em></p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- API Keys ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

model = genai.GenerativeModel("gemini-2.0-flash")

# --- State Init ---
if "vibe_history" not in st.session_state:
    st.session_state.vibe_history = []
if "current_playlist" not in st.session_state:
    st.session_state.current_playlist = []

# --- Mood Input ---
user_mood = st.text_input("What's your mood? 🧠💭", placeholder="E.g., heartbroken, excited, chaotic, sleepy...")

# --- Prompt Builder ---
def create_prompt(mood):
    return f"""
You are VibeDJ — an AI that creates perfect music playlists based on the user's current mood. 
You're cool, emotionally intelligent, and have dangerously good taste in music.
NEVER explain the playlist. Just give:
- A creative playlist title
- A matching emoji or two
- A list of 5-8 song titles and artists that match the mood (in format: Title – Artist)
Mood: {mood}
Playlist:
"""

# --- Spotify Search ---
def search_track_preview(query):
    results = sp.search(q=query, limit=1, type='track')
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        return {
            "title": f"{track['name']} – {track['artists'][0]['name']}",
            "preview_url": track["preview_url"],
            "spotify_url": track["external_urls"]["spotify"]
        }
    return None

# --- Playlist Generation Logic ---
if user_mood:
    with st.spinner("Finding your vibe..."):
        prompt = create_prompt(user_mood)
        gemini_output = model.generate_content(prompt).text.strip()

        st.session_state.vibe_history.append(("Mood", user_mood))
        st.session_state.vibe_history.append(("Playlist", gemini_output))

        # Extract songs
        lines = gemini_output.splitlines()
        tracks = [line for line in lines if "–" in line]

        playlist = []
        for song in tracks:
            track = search_track_preview(song.strip())
            if track:
                playlist.append(track)

        st.session_state.current_playlist = playlist

# --- Show Playlist ---
if st.session_state.current_playlist:
    st.markdown("### 🎶 Your Playlist")
    for track in st.session_state.current_playlist:
        st.markdown(f"**{track['title']}**")
        if track["preview_url"]:
            st.audio(track["preview_url"])
        st.markdown(f"[Open on Spotify]({track['spotify_url']})")
        st.markdown("---")

    # --- Format Selector ---
    st.markdown("### ⬇️ Download Your Playlist")
    file_format = st.selectbox("Choose format", ["JSON", "CSV", "TXT"])

    # --- JSON Format ---
    if file_format == "JSON":
        playlist_json = json.dumps(st.session_state.current_playlist, indent=2)
        st.download_button(
            label="💾 Download JSON",
            data=playlist_json,
            file_name="vibedj_playlist.json",
            mime="application/json"
        )

    # --- CSV Format ---
    elif file_format == "CSV":
        df = pd.DataFrame(st.session_state.current_playlist)
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name="vibedj_playlist.csv",
            mime="text/csv"
        )

    # --- TXT Format ---
    elif file_format == "TXT":
        txt_data = "\n".join(
            f"{track['title']} - {track['spotify_url']}" for track in st.session_state.current_playlist
        )
        st.download_button(
            label="📃 Download TXT",
            data=txt_data,
            file_name="vibedj_playlist.txt",
            mime="text/plain"
        )

    # --- Optional: Spotify Export (Open All)
    with st.expander("🎧 Open all songs in Spotify"):
        for track in st.session_state.current_playlist:
            st.markdown(f"- [{track['title']}]({track['spotify_url']})")

# --- Footer ---
st.markdown("---")
st.markdown("*“You bring the feels. I bring the beats.”* 🎵")
st.caption("Built with 🎧, APIs, and late-night vibes.")
