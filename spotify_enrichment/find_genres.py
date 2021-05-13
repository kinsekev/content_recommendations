import os
import sys
import spotipy
import spotipy.util as util
import pandas as pd

tracks = pd.read_csv('./data/tracks_data.csv')

genres = []

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
    track = spotify_object.track(track_id=tracks['track_uri'][i])
    artist_id = track['artists'][0]['id']
    artist = spotify_object.artist(artist_id=artist_id)
    
    if artist['genres']:
        genre = '|'.join(artist['genres'])
        print(genre)
        genres.append(genre)
    else:
        genres.append('')

tracks['genres'] = genres
tracks = tracks[tracks['genres'].notnull()]
tracks.to_csv('./data/tracks_data.csv', index=False)