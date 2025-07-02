# imported libraries and classes/functions
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import sys
import re

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "http://127.0.0.1:8888/callback"

# Define the scopes (permissions you're asking the user to allow)
SCOPE = "playlist-modify-private playlist-modify-public user-read-private"

# Create a Spotify object with OAuth
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
    )
)


# lists to save user's liked and disliked ssongs
favorites = []
not_favorites = []


# my main function
def main():
    print("\n✨ Welcome to my MOOD-SONG WIZARD! 🎵🧙‍♂️")
    print("➡️ Tell me how you feel and I will recommend a song to you.\n")

    mood = get_user_mood()
    recommendation = display_recommendation(mood)
    handle_user_feedback(mood, recommendation)


# Get the user's mood
def get_user_mood():
    while True:
        mood = input("How are you feeling today 🙃: ").strip().lower()

        if not re.fullmatch(r"^[a-zA-Z ]+", mood):
            print("No numbers allowed please! Try again\n")
            continue

        return mood


# song recommendation function
def recommend_song(mood):
    try:
        result = sp.search(
            q=mood, type="track", limit=50, offset=50
        )  # this is a very huge dictionary of 50 tracks
        tracks = result["tracks"]  # I have indexed into tracks
        all_tracks = tracks["items"]  # I have indexed into items (tracks/items) -- list

        # if Spotify could not find a match...
        if not all_tracks:
            return ["No song found", "N/A", "https://spotify.com"]

        # pick a random track from the top 10 Spotify returns for mood
        track = random.choice(all_tracks)

        # for artists
        album = track["album"]
        artists = album["artists"]
        artists_one = artists[0]
        artist_name = artists_one["name"]

        # for song name
        song_name = track["name"]

        # song url
        song_url = track["external_urls"]["spotify"]

        return [song_name, artist_name, song_url]  # I am returning a list

    except Exception as e:
        print(f"Spotify lookup failed: {e}")
        return ["No song found", "N/A", "https://spotify.com"]


# program response to user's mood
def display_recommendation(mood):
    recommendation = recommend_song(mood)
    # this get's the return value of 'recommend_song(mood)' function

    if not recommendation or len(recommendation) != 3:
        print("😕 Couldn't find a valid song recommendation.")
        return ["No song found", "N/A", "https://spotify.com"]

    song, artist, url = [
        i.strip() for i in recommendation
    ]  # basically strip white space from each item in the list

    # side effects here
    print(f"\n⭐ Mood: {mood.capitalize()}")
    print(f"🎧 My recommendation: '{song}' by '{artist}'")
    print(f"🔗 Listen here: {url}")

    # the return value of this function
    return [
        song,
        artist,
        url,
    ]  # I am returning this to make this function reusable later on


# User feedback function
def handle_user_feedback(mood, last_recommendation):
    count = 0

    while True:
        print("\nWe'd love to know what you think 🙃")
        feedback = input("Did you like it: ").strip()

        if feedback.capitalize() == "No":
            print("\nLet's try another, shall we? 🤔")

            # saves the not liked recommendation to 'Not Favorites.txt'
            not_favorites.append(last_recommendation)

            try:
                song, artist, url = last_recommendation
            except (TypeError, ValueError):
                song, artist, url = "Unknown", "N/A", "https://spotify.com"

            with open("Not Favorites.txt", "a") as file:
                file.write(f"{song} by {artist} - {url}\n")

            # this is the previous recommendation
            last_recommendation = display_recommendation(mood)
            count += 1

            if count == 2:
                print()
                print("=" * 80)
                print("Next steps:")
                print("Enter 'Yes' for another recommendation")
                print("Enter 'No' to exit the program")
                print("Or enter 'Quit' to quit the program safely")
                print("=" * 80)

                more = input(
                    "\nWould you still like some more recommendations? "
                ).strip()

                if more.capitalize() == "Yes":
                    print("\nLet's find a good one this time, shall we? 🤔💭 🤔💭")
                    last_recommendation = display_recommendation(mood)
                    # saves the last recommendation
                    continue  # ask for feedback again in main loop

                elif more.capitalize() == "No":
                    print()
                    print("-" * 80)
                    sys.exit(
                        "We are sorry we couldn't find what you were looking for 😔"
                    )

                elif more.capitalize() == "Quit":
                    print()
                    print("-" * 80)
                    print(
                        f"Make sure to check 'Favorites.txt' for your liked songs and 'Not Favorites' for disliked songs. 🎧🎵"
                    )
                    sys.exit("\nThank you for listening. Come back soon! 👋")

                else:
                    print("\nPlease try either 'Yes', 'No', or 'Quit'.")
                    continue

        elif feedback.capitalize() == "Yes":
            print("\nThat's lovely! 😊")

            # saves the liked recommendation to 'Favorites.txt'
            favorites.append(last_recommendation)

            try:
                song, artist, url = last_recommendation
            except (TypeError, ValueError):
                song, artist, url = "Unknown", "N/A", "https://spotify.com"

            with open("Favorites.txt", "a") as file:
                file.write(f"{song} by {artist} - {url}\n")

            # Create real playlist in user's account and add liked songs
            playlist_id = get_or_create_favorites_playlist(sp)
            uri = get_track_uri(song, artist)

            if uri:
                sp.playlist_add_items(playlist_id, [uri])
                print(f"✅ Added to your Spotify playlist: {song} by {artist}")
            else:
                print(f"⚠️ Could not find track URI for '{song}' by '{artist}'")

            while True:
                another = input("\nWould you like another? ").strip()

                if another.capitalize() == "No":
                    print(
                        f"\nMake sure to check 'Favorites.txt' for your favorite songs and 'Not Favorites' for disliked songs."
                    )
                    sys.exit("\nThank you for listening. Come back soon! 👋")

                elif another.capitalize() == "Yes":
                    print("\nHere is another recommendation 🙂🎶")
                    last_recommendation = display_recommendation(mood)
                    break  # back to main loop for feedback

                else:
                    print("Please choose either 'Yes' or 'No'")
                    continue
        else:
            print("Please answer with 'Yes' or 'No'")
            continue


def get_or_create_favorites_playlist(sp):
    user_id = sp.current_user()["id"]
    playlists = sp.current_user_playlists()["items"]

    for playlist in playlists:
        if playlist["name"].lower() == "favorites":
            return playlist["id"]

    new_playlist = sp.user_playlist_create(
        user=user_id,
        name="Favorites",
        public=False,
        description="Songs I liked from the Mood Wizard 🎵",
    )
    return new_playlist["id"]


def get_track_uri(song_name, artist_name):
    query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=query, type="track", limit=1)

    items = results["tracks"]["items"]
    if items:
        return items[0]["uri"]
    return None


if __name__ == "__main__":
    main()
