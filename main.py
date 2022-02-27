import spotipy
from spotipy.oauth2 import SpotifyOAuth


def spotify_init():
    scope = 'user-top-read'
    f = open('client_info2.txt', 'r')
    CLIENT_ID = f.readline().strip()
    CLIENT_SECRET = f.readline().strip()
    REDIRECT_URI = f.readline().strip()
    f.close()
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=scope
        )
    )


def main():
    sp = spotify_init()
    r = sp.current_user_top_tracks(20, 0, "medium_term")
    d = []
    for track in r['items']:
        track_name = track['name']
        track_artist_name = track['artists'][0]['name']
        print(track_name, track_artist_name, sep=' - ')


if __name__ == '__main__':
    main()