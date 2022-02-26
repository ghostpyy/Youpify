import requests
import base64
import datetime


class Client:
    _client_id = None
    _client_secret = None
    _client_creds_b64 = None
    _access_token = None
    _access_token_expires = datetime.datetime.now()

    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret
        creds = f"{client_id}:{client_secret}"
        self._client_creds_b64 = base64.b64encode(creds.encode())

    def check_access_token_expiry(self) -> bool:
        now = datetime.datetime.now()
        return self._access_token_expires < now

    def get_access_token(self):
        if self.check_access_token_expiry():
            if not self._auth():
                exit(1)
        return self._access_token

    def _auth(self):
        if self._client_id is None:
            exit(1)
        token_url = "https://accounts.spotify.com/api/token"
        token_data = {
            "grant_type": "client_credentials"
        }
        token_header = {
            "Authorization": f"Basic {self._client_creds_b64.decode()}"
        }
        r = requests.post(token_url, data=token_data, headers=token_header)
        data = r.json()
        # print(data)
        if r.status_code not in range(200, 299):
            print("auth error")
            return False

        self._access_token = data['access_token']
        now = datetime.datetime.now()
        expires_in = data['expires_in']
        self._access_token_expires = now + datetime.timedelta(seconds=expires_in)
        return True
