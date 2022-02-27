import google_auth_oauthlib.flow
import googleapiclient.discovery
import spotipy
from spotipy.oauth2 import SpotifyOAuth


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


def main():
    sp = spotify_init()
    spotify_request = sp.current_user_top_tracks(20, 0, "medium_term")
    top_tracks = []
    for track in spotify_request['items']:
        track_name = track['name']
        track_artist_name = track['artists'][0]['name']
        top_tracks.append((track_name, track_artist_name))

    yt = youtube_init()
    create_playlist = yt.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Top Spotify tracks playlist",
                "description": "Created for UCI Hackathon 2022",
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "private"
            },
        }
    )
    response_create_playlist = create_playlist.execute()
    print(response_create_playlist)
    for track in top_tracks:
        request_song = yt.search().list(
            part="snippet",
            maxResults=1,
            q=track[0] + ' ' + track[1]
        )
        song_response = request_song.execute()
        add_video_request = yt.playlistItems().insert(
            part="snippet,status",
            body={
                'snippet': {
                    'playlistId': response_create_playlist['id'],
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': song_response['items'][0]['id']['videoId']
                    }
                }
            }
        )
        add_video_request.execute()


if __name__ == '__main__':
    main()
