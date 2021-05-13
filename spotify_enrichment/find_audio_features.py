import os
import sys
import spotipy
import spotipy.util as util
import pandas as pd

tracks = pd.read_csv('./data/tracks_data.csv')

acousticness = []
danceability = []
energy = []
instrumentalness = []
liveness = []
loudness = []
speechiness = []
tempo = []
valence = []

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

for i in range(0, len(tracks), 100):

    # get track ids from tracks df
    track_uri = tracks['t_uri'][i:i+100].tolist()

    # call 100 track uris to audio_features
    features = spotify_object.audio_features(tracks=track_uri)

    for feature in features:
        if feature:
            # acousticness
            acousticness.append(feature['acousticness'])
            # danceability
            danceability.append(feature['danceability'])
            # energy
            energy.append(feature['energy'])
            # instrumentalness
            instrumentalness.append(feature['instrumentalness'])
            # liveness
            liveness.append(feature['liveness'])
            # loudness
            loudness.append(feature['loudness'])
            # speechiness
            speechiness.append(feature['speechiness'])
            # tempo
            tempo.append(feature['tempo'])
            # valence
            valence.append(feature['valence'])
        else:
            # acousticness
            acousticness.append('')
            # danceability
            danceability.append('')
            # energy
            energy.append('')
            # instrumentalness
            instrumentalness.append('')
            # liveness
            liveness.append('')
            # loudness
            loudness.append('')
            # speechiness
            speechiness.append('')
            # tempo
            tempo.append('')
            # valence
            valence.append('')

# add columns to dataframe
tracks['acousticness'] = acousticness
tracks['danceability'] = danceability
tracks['energy'] = energy
tracks['instrumentalness'] = instrumentalness
tracks['liveness'] = liveness
tracks['loudness'] = loudness
tracks['speechiness'] = speechiness
tracks['tempo'] = tempo
tracks['valence'] = valence

# filter null rows
tracks = tracks[tracks['acousticness'].notnull()]
tracks = tracks[tracks['danceability'].notnull()]
tracks = tracks[tracks['energy'].notnull()]
tracks = tracks[tracks['instrumentalness'].notnull()]
tracks = tracks[tracks['liveness'].notnull()]
tracks = tracks[tracks['loudness'].notnull()]
tracks = tracks[tracks['speechiness'].notnull()]
tracks = tracks[tracks['tempo'].notnull()]
tracks = tracks[tracks['valence'].notnull()]

tracks.to_csv('./data/tracks_data.csv', index=False)