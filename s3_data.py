
import pandas as pd

files = [pd.read_csv('./user_data/part-0000' + str(i) + '-ee21a60e-0148-43ca-af1a-2e0863f52264-c000.csv') for i in range(10)] + \
        [pd.read_csv('./user_data/part-000' + str(i) + '-ee21a60e-0148-43ca-af1a-2e0863f52264-c000.csv') for i in range(10, 31)]
df = pd.concat(files)

# filter out null values in artists, albums and tracks

df = df[df['artist_name'].notnull()]
df = df[df['album_name'].notnull()]
df = df[df['track_name'].notnull()]

# filter artist names with 'Intro' or 'Untitled'
df = df[df['artist_name'] != 'Intro']
df = df[df['artist_name'] != 'Untitled']

# filter album names with 'Intro' or 'Untitled'
df = df[df['album_name'] != 'Intro']
df = df[df['album_name'] != 'Untitled']

# filter track names with 'Intro' or 'Untitled'
df = df[df['track_name'] != 'Intro']
df = df[df['track_name'] != 'Untitled']

print(df.info())

# count the tracks in dataset
dct = {}
for track_name in df['track_name'].tolist():
    if track_name in dct:
        dct[track_name] += 1
    else:
        dct[track_name] = 1

# filter down to popular tracks
pop_tracks = {k: v for k, v in sorted(dct.items(), key=lambda x: x[1], reverse=True) if v > 150}
df = df[df['track_name'].isin(pop_tracks)]

# drop duplicate artist_name, track_name
df = df.drop_duplicates(['artist_name', 'track_name'])

# select artist_name, album_nmae, track_name
df = df[['artist_name', 'album_name', 'track_name']]

# create search term column
df['search_term'] = df['artist_name'] + ', ' + df['track_name']

# tracks
df.to_csv('./data/tracks_data.csv', index=False)