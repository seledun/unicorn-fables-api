from keys import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from base64 import b64encode
import requests

spotify_client_id = SPOTIFY_CLIENT_ID
spotify_client_secret = SPOTIFY_CLIENT_SECRET

# Sends a request to Spotify to get an authorization token
# Returns the token as a string on success
def get_spotify_token() -> str:
    auth_str = f"{spotify_client_id}:{spotify_client_secret}"
    base64_auth_str = b64encode(auth_str.encode()).decode('utf-8')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {base64_auth_str}'
    }

    payload = {
        'grant_type': 'client_credentials'
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=payload)
    data = response.json()
    
    return data['access_token']

# Sends authorization token and formatted query to Spotify
# Returns the track uri as a string on success
def spotify_search(token, query) -> str:
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=track&limit=1', headers=headers)
    data = response.json()

    resp = data['tracks']['items'][0]['uri'] # Get track uri
    return resp