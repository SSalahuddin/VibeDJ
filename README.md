# 🎧 VibeDJ: A Playlist Generator That Feels Your Mood

## 💡 Inspiration

Music is therapy. But choosing the right songs when you're in your *feels*? Emotionally exhausting.
We wanted to build something that listens to your emotions — and instantly responds with music that gets it.

**VibeDJ** was inspired by:

* The struggle of finding the *right* song for every mood.
* The idea that AI can be a vibe-curator, not just a fact-spewer.
* A love for both sarcasm and serious jams — and the desire to turn moods into music instantly.

## 🎶 What It Does

**VibeDJ** is a mood-to-music playlist generator powered by:

* **Gemini** (Google Generative AI) for creative playlist curation
* **Spotify Web API** for real song previews and track links
* **Streamlit** for a fast, fun user interface

You type your mood — happy, heartbroken, chaotic, gym-raging, sleepy, anything — and it responds with:

* A unique playlist title and emoji
* 5–8 song recommendations (via Spotify)
* 30-second playable previews
* Options to download your playlist in `.json`, `.csv`, or `.txt` formats

## 🛠️ How We Built It

We built **VibeDJ** using:

* `streamlit`: frontend UI and deployment
* `google-generativeai`: to prompt Gemini to generate human-like, themed playlists
* `spotipy`: to search songs and retrieve Spotify preview URLs
* `pandas`: for converting playlists to downloadable formats

### Workflow:

1. User enters their mood via a text input.
2. A few-shot prompt is sent to Gemini to generate a themed playlist (e.g., sad breakup → Adele, Lorde, etc.).
3. Each generated song is searched via Spotify API to get:

   * Title
   * Artist
   * 30s audio preview
   * Direct Spotify link
4. Users see the playlist, preview songs, and download it in their preferred format.


## 🧱 Challenges We Ran Into

* **Parsing Gemini’s output** into usable song names required careful pattern matching.
* Not every track had a Spotify preview URL — we had to gracefully skip or substitute.
* Streamlit's file handling is **stateless** — we moved to dynamic download buttons using `st.download_button`.
* Spotify’s redirect URI requirement added friction (though resolved with a dummy HTTPS URI).

## 🏆 Accomplishments That We're Proud Of

* Creating **vibe-responsive playlists** that genuinely *feel* emotionally accurate
* Seamless integration of multiple APIs in a lightweight app
* Giving users actual playable previews in the browser with clean formatting
* Making it **fun and human**, not just functional

## 📚 What We Learned

* Gemini performs much better with **few-shot prompting** and styled tone control
* Spotipy’s Client Credentials Flow is perfect for music search without login
* Streamlit is incredibly fast to prototype — and fun to design expressive apps in
* UI/UX matters — even little things like emoji and tone made the bot feel alive 🎭

Also, math is hard, but music is math.
Even if we didn’t write any equations, we felt the rhythm like $y = \sin(x)$.


## 🚀 What's Next for VibeDJ

Here’s what we’re planning next:

* Let users **save playlists to their Spotify account** (OAuth flow)
* Add **predefined mood buttons**: 🎉 Party, 💔 Breakup, ☕ Chill, 🧠 Study
* Add **image generation** (e.g., playlist covers using AI)
* Integrate **emotion detection from journal text** (combo with CryPal bot?)
* Support **collaborative playlists**: share a mood, get a group playlist


**Try it now:** [https://huggingface.co/spaces/Sumayyea/VibeDJ](https://huggingface.co/spaces/Sumayyea/VibeDJ)
*“You bring the feels. I bring the beats.”* 🎧

