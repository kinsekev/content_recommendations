import pandas as pd
from sklearn import preprocessing

# load tracks data
tracks = pd.read_csv('./tracks_data.csv')

# load listening events 
files = [pd.read_csv('./user_data/part-0000' + str(i) + '-ee21a60e-0148-43ca-af1a-2e0863f52264-c000.csv') for i in range(10)] + \
        [pd.read_csv('./user_data/part-000' + str(i) + '-ee21a60e-0148-43ca-af1a-2e0863f52264-c000.csv') for i in range(10, 31)]
levents = pd.concat(files)

##############################################################################
# tracks
# take random sample of 12000 from tracks
tracks = tracks.sample(12000)

# parse track-uri
tracks['t_uri'] = tracks['track_uri'].str.split(':').str[-1]

# scale the tempo variable
min_max_scaler = preprocessing.MinMaxScaler()
tracks['tempo'] = min_max_scaler.fit_transform(tracks[['tempo']])

# filter genres
f_genres = ['rock', 'metal', 'dance', 'pop', 'indie', 'folk', 'hip hop', 
            'electronica', 'blues', 'jazz', 'soul', 'r&b', 'rap', 'edm', 
            'classical', 'disco']


def filter_genres(row):
    filtered_genres = []
    genres = row['genres'].split('|')
    
    for f_genre in f_genres:
        for genre in genres:
            if f_genre in genre:
                filtered_genres.append(f_genre)
                
    if filtered_genres:
        return '|'.join(set(filtered_genres))
    return None


tracks['filtered_genres'] = tracks.apply(filter_genres, axis=1)

##############################################################################
# ratings
merged = pd.merge(levents, tracks, how='inner', on=['artist_name', 'track_name'])

ratings = merged[['user_id', 't_uri', 'timestamp']]

ratings['rating'] = 1
ratings = ratings[['user_id', 't_uri', 'rating', 'timestamp']]

##############################################################################

tracks.to_csv('./data/tracks_data.csv', index=False)
ratings.to_csv('./data/ratings_data.csv', index=False)