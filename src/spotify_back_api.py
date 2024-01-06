import requests
from base64 import b64encode
from keys import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Import API keys
spotify_client_id = SPOTIFY_CLIENT_ID
spotify_client_secret = SPOTIFY_CLIENT_SECRET


def get_spotify_token():
    print("SPOTIFY!")

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


def spotify_search(token, query):
    print("Inside searchTrack:", query)
    print(f'https://api.spotify.com/v1/search?q={query}&type=track')
    print(token)

    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=track', headers=headers)
    data = response.json()

    return data


# Example of using the functions
if __name__ == "__main__":
    spotify_token = get_spotify_token()
    search_result = spotify_search(spotify_token, "your_query_here")

    print(search_result)
