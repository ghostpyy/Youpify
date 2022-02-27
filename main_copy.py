import time

import google_auth_oauthlib.flow
import googleapiclient.discovery
import spotipy
from spotipy.oauth2 import SpotifyOAuth


SLEEP_INTERVAL = 1
TOP_TRACK_CNT = 5


def spotify_init():
    scope = 'user-top-read'
    f = open('client_info.txt', 'r')
    client_id = f.readline().strip()
    client_secret = f.readline().strip()
    redirect_uri = f.readline().strip()
    f.close()
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope
        )
    )


def youtube_init():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"
    scopes = ["https://www.googleapis.com/auth/youtube"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )
    credentials = flow.run_local_server()
    return googleapiclient.discovery.build(
        api_service_name,
        api_version,
        credentials=credentials
    )


def get_top_spotify(sp, track_cnt: int):
    spotify_request = sp.current_user_top_tracks(track_cnt, 0, "medium_term")
    top_tracks = []
    for track in spotify_request['items']:
        track_name = track['name']
        track_artist_name = track['artists'][0]['name']
        top_tracks.append((track_name, track_artist_name))
    return top_tracks


def get_tracks_spotify_playlist(sp, playlist_id):
    tracks = []
    playlist_tracks = sp.playlist_items(playlist_id=playlist_id, additional_types=["track"])
    for track in playlist_tracks['items']:
        track_name = track['track']['name']
        track_artist_name = track['track']['artists'][0]['name']
        tracks.append((track_name, track_artist_name))
    return tracks


def create_new_yt_playlist(yt, playlist_title):
    create_playlist = yt.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_title,
                "description": "Created for UCI Hackathon 2022",
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "private"
            },
        }
    )
    response_create_playlist = create_playlist.execute()
    return response_create_playlist['id']


def add_to_yt_playlist(yt, playlist_id, top_tracks):
    for track in top_tracks:
        request_song = yt.search().list(
            part="snippet",
            maxResults=1,
            q=track[0] + ' ' + track[1]
        )
        time.sleep(SLEEP_INTERVAL)
        song_response = request_song.execute()
        video_id = song_response['items'][0]['id']['videoId']

        add_video_request = yt.playlistItems().insert(
            part="snippet,status",
            body={
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        )
        time.sleep(SLEEP_INTERVAL)
        response = add_video_request.execute()


def conv_playlist_spotify_youtube(sp, yt, playlist_id):
    tracks = get_tracks_spotify_playlist(sp, playlist_id)
    yt_playlist_id = create_new_yt_playlist(yt, "Spotify Playlist")
    add_to_yt_playlist(yt, yt_playlist_id, tracks)


def main():
    sp = spotify_init()
    yt = youtube_init()

    # convert a spotify playlist to a YouTube playlist
    # playlist_url = 'https://open.spotify.com/playlist/5FvzeSjMVp0xYt9loCuP8A'
    playlist_url = 'https://open.spotify.com/playlist/4sjcxbRlA4E4cb9XgxozsB'
    playlist_id = playlist_url.split('/')[-1]
    conv_playlist_spotify_youtube(sp, yt, playlist_id)

    # convert top spotify tracks to a YouTube playlist
    # top_tracks = get_top_spotify(sp, TOP_TRACK_CNT)
    # new_playlist_id = create_new_yt_playlist(yt, "Top Spotify Tracks")
    # add_to_yt_playlist(yt, new_playlist_id, top_tracks)


if __name__ == '__main__':
    main()
