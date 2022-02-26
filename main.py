import requests

import client


def main():
    f = open("client_info.txt")
    client_id = f.readline().strip()
    client_secret = f.readline().strip()
    # print(client_id, client_secret)
    test_client = client.Client(client_id, client_secret)
    token = test_client.get_access_token()
    # print(token)

    # token won't be returned if the query window is too early
    # in that case, use previous value
    if token is None:
        token = f.readline().strip()
        f.close()
    else:
        f.close()
        w = open('client_info.txt', 'w')
        w.write(client_id + '\n' + client_secret + '\n' + token)
        w.close()

    test_playlist_link = 'https://open.spotify.com/playlist/3j8LBB0fzGoyCjutd91Te6'
    test_playlist_code = test_playlist_link.split("/")[-1]
    # print(test_playlist_code)
    url = f"https://api.spotify.com/v1/playlists/{test_playlist_code}/tracks"
    header = {
        "Authorization": f"Bearer {token}"
    }
    r = requests.get(url, headers=header)
    data = r.json()
    for track in data['items']:
        print(track['track']['name'])


if __name__ == '__main__':
    main()
