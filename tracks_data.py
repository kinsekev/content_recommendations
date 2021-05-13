import csv

TRACKS_FILEPATH = './data/tracks_data.csv'


def convert_track_id_names():
    dct = {}
    with open(TRACKS_FILEPATH, newline='', encoding='utf-8') as tracks:
        tracks_reader = csv.reader(tracks)
        for row in tracks_reader:
            track_uri = row[5]
            track_name = row[0] + ', ' + row[2]
            dct[track_uri] = track_name
    return dct


def get_audio_features():
    audio_features = {}
    with open(TRACKS_FILEPATH, newline='', encoding='utf-8') as tracks:
        tracks_reader = csv.reader(tracks)
        next(tracks_reader)
        for row in tracks_reader:
            track_uri = row[5]
            acousticness = float(row[9])
            danceability = float(row[10])
            energy = float(row[11])
            instrumentalness = float(row[12])
            liveness = float(row[13])
            speechiness = float(row[15])
            tempo = float(row[16])
            valence = float(row[17])
            audio_features[track_uri] = [
                acousticness,
                danceability,
                energy,
                instrumentalness,
                liveness,
                speechiness,
                tempo,
                valence
            ]
    return audio_features


def get_genres():
    genres = {}
    genres_lookup = {}
    total_genres = 0
    
    with open(TRACKS_FILEPATH, newline='', encoding='utf-8') as tracks:
        tracks_reader = csv.reader(tracks)
        next(tracks_reader)
        for row in tracks_reader:
            track_uri = row[5]
            cur_genres = row[7].split('|')
            cur_genres_lst = []
            for cur_genre in cur_genres:
                if cur_genre in genres_lookup:
                    genre_num = genres_lookup[cur_genre]
                else:
                    genre_num = total_genres
                    genres_lookup[cur_genre] = genre_num
                    total_genres += 1
                cur_genres_lst.append(genre_num)
            genres[track_uri] = cur_genres_lst
    
    for track_uri, genres_lst in genres.items():
        dimensions = [0] * total_genres
        for genre_num in genres_lst:
            dimensions[genre_num] = 1
        genres[track_uri] = dimensions
    
    return genres
    