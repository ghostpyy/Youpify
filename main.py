import spotipy
from spotipy.oauth2 import SpotifyOAuth


def main():
    scope = 'user-top-read'
    f = open('client_info2.txt', 'r')
    CLIENT_ID = f.readline().strip()
    CLIENT_SECRET = f.readline().strip()
    REDIRECT_URI = f.readline().strip()
    f.close()
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=scope
        )
    )
    r = sp.current_user_top_tracks()
    for track in r['items']:
        print(track['name'], track['artists'][0]['name'], sep=' - ')


if __name__ == '__main__':
    main()