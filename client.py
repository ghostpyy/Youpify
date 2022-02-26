import requests
import base64
import datetime


class Client:
    client_id = None
    client_secret = None
    client_creds_b64 = None
    access_token = None
    access_token_expires = datetime.datetime.now()

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        creds = f"{client_id}:{client_secret}"
        self.client_creds_b64 = base64.b64encode(creds.encode())

    def check_access_token_expiry(self):
        now = datetime.datetime.now()
        return self.access_token_expires < now

    def get_access_token(self):
        if self.check_access_token_expiry():
            self.auth()
        return self.access_token

    def auth(self):
        if self.client_id is None:
            return False
        token_url = "https://accounts.spotify.com/api/token"
        token_data = {
            "grant_type": "client_credentials"
        }
        token_header = {
            "Authorization": f"Basic {self.client_creds_b64.decode()}"
        }
        r = requests.post(token_url, data=token_data, headers=token_header)
        data = r.json()
        # print(data)
        if r.status_code not in range(200, 299):
            print("auth error")
            return False

        self.access_token = data['access_token']
        now = datetime.datetime.now()
        expires_in = data['expires_in']
        self.access_token_expires = now + datetime.timedelta(seconds=expires_in)
        return True
