# MOOD-SONG WIZARD 🎵🧙‍♂️  
#### Video Demo: https://youtu.be/Ar28i-HlCp8
#### Description:

We humans experience a wide range of emotions, and it’s important to acknowledge and embrace them. This project, “Mood-Song Wizard,” is a command-line program that functions like a mini therapist — one that speaks the universal language of music. Given a user's mood, it uses the Spotify API to fetch songs related to that mood and recommends one at random. The user is then prompted for feedback, and the response is recorded in a report file for future reference.

This project was written entirely in Python and makes use of the third-party `Spotipy` library to interact with the Spotify API. It leverages either of two authentication flows depending on developer preference: the **Client Credentials Flow** (not used here) or the **Authorization Code Flow** (used in this upload). The former provides access to Spotify’s public catalog of songs anonymously, while the latter would allow for actual changes to a logged-in user’s account — such as creating playlists and adding tracks in real-time.

---

## Project Structure and Files:

- `project.py`: This is the main program. It begins by prompting the user to describe how they're feeling. The input is validated to ensure it contains no numbers or unsupported characters. The program then uses Spotify’s search endpoint to retrieve the top 50 tracks related to that mood. A single track is chosen randomly, and the program outputs its name, artist, and a clickable URL that leads to the song on Spotify.

  After the recommendation, the program asks the user whether they liked the song. If they respond "Yes", the song is saved to a local file called `Favorites.txt`. If they respond "No", the song is instead saved to `Not Favorites.txt`. These files serve as a session report, allowing the user (or developer) to review their preferences later.

  In this code, with the Authorization Code Flow enabled, liked songs can also be added to the user’s Spotify account via a new or existing playlist titled "Favorites".

- `Favorites.txt` and `Not Favorites.txt`: These are the two simple output files created during user sessions. They log the songs that were liked or disliked by the user, including song title, artist, and a Spotify URL.

- `README.md`: This file provides a comprehensive overview of the project, its functionality, files, design decisions, and usage.

- `requirements.txt`: Lists all Python packages required to run the program (namely `spotipy` and `black` for formatting).

---

## Design Considerations:

I used emojis extensively throughout the CLI to simulate a more engaging, GUI-like experience. Feedback prompts, song output, and even error messages are styled in a way that brings personality and polish to an otherwise text-only program.

I also ensured that my code was readable and maintainable. Long lines were broken up and reformatted using the `black` module. I added comments throughout the code to explain each section clearly — both for my own understanding and for anyone else who might read or use this project.

---

## License:

This project is intended for academic use only. Please replace the included 'client_id' and 'client_secret' with your own if testing.

The client id and client secret used in my project were obtained after I created a app in Spotify at 'Spotify for Devlopers' - "https://developer.spotify.com/" (Log in with Spotify account)

In this context, an “app” refers to the platform Spotify provides for hosting and authenticating your program. The client_id and client_secret are like your app’s username and password — used to authenticate your application (not you personally) when accessing Spotify’s Web API via Spotipy.

- client_id      # A unique identifier for your Spotify developer app
- client_secret  # A secret key proving your app is legit (keep it safe!)

---

## Final Thoughts:

This was an intelletually stimulating experience for me building and running this program. I hope you enjoy it as much as I did working on it.

---
