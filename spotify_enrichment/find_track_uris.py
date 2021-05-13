import os
import sys
import spotipy
import spotipy.util as util
import pandas as pd

tracks = pd.read_csv('./tracks_data.csv')

track_uri = []

# Get the username from terminal
username = sys.argv[1]
os.remove(f".cache-{username}")

# Erase cache and prompt and user permission
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

spotify_object = spotipy.Spotify(auth=token)

for i in range(len(tracks)):
    track = spotify_object.search(q=tracks['search_term'][i], limit=1, offset=0, type='track')
    if track['tracks']['items']:
        print(track['tracks']['items'][0]['uri'])
        track_uri.append(track['tracks']['items'][0]['uri'])
    else:
        track_uri.append('')

tracks['track_uri'] = track_uri
tracks = tracks[tracks['track_uri'].notnull()]
tracks.to_csv('./data/tracks_data.csv', index=False)
