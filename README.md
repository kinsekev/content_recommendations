
# Conent Based Recommendation System

This project uses the LFM-1b dataset along with the Spotify API as sources of data for the recommendation system. 
In this project a sample of 12000 unique tracks are taken from the LFM-1b dataset and are collated with the users who listened to these tracks.
Further, each of the 12000 tracks are enriched with the Spotify API to find content-based features for acousticness, danceability, energy, instrumentalness,
liveness, loudness, speechiness, tempo, valence and genres. Using these features a content-based similarity is found between tracks by using the cosine method. 
Track recommmendations are given to users based off of similarity from their previous listening history.

# Requirements

```
pip install numpy
pip install pandas
pip install matplotlib
pip install pyspark
pip install spotipy
```

# Running the code

## Getting the dataset from LFM-1b

Due to the size of the LFM-1b dataset, the spark_get_data.py file must be run on a cluster such as AWS with Hadoop and PySpark. The spark_get_data.py script reads 
in each of the files (users, artists, albums, tracks and listening events) as spark dataframes and joins each of the tables to collect all of the data.
Finally, it selects a fraction of the combinded dataframe and writes the dataframe to a CSV file.

```
python spark_get_data.py
```


## Clean data set

The s3_data.py script, cleans the data obtained in the previous script and creates a tracks dataset containing unique tracks. 
It first reads in the files, filters out unwanted tracks, find tracks that have been listened to by over 150 users, drops the duplicate rows and adds a search term 
(artist name + track name) which will be used to search the Spotify API with. Finally, this dataframe is written to a CSV file.

To run the code:
```
python s3_data.py
```

## Spotify Enrichment

The Spotify enrichment involves 3 steps, first find the the track uri from the Spotify API by searching for the search term created in the previous section. Using the found track uri,
again search the Spotify API for the audio features (acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, valence). Similarly search the track uri
to find the genres associated with the tracks.

To run the code:
```
python spotify_enrichment/find_track_uris.py
python spotify_enrichment/find_audio_features.py
python spotify_enrichment/find_genres.py
```

## Enrirch data, generate tracks and ratings files 

The Python Surprise package requires a ratings dataset with a user-id, track-uri and rating which is created with this script. The tracks data set is also modified by selecting a sample of 
12000 unique tracks (to run on local hardware) and the number of genres are filtered down to 16 groups. To create the ratings dataset, merge the original listening events file with the enriched 
tracks data, this will return a file with 12000 unique tracks with approx 1000 different users. The tracks and ratings files are written to CSV.

## Enrich the data set

To run the code:
```
python ratings_track_files.py
```

## Predictions

In order to generate the predictions for the recommendation system, run the metrics.py file. This reads in the ratings data set, builds the similarity matrix finding similarities
between each pair of tracks. Similarity is found by computing the cosine between each pair of tracks audio features, geners or both to give a score. To give a prediction to a user
for a given track, the estimate method finds all of the tracks the user has listened to and computes the similarities of these tracks with the unheard track. The k-nearest neighbours 
are choosen and these scored are summed and divided by k. A track is similar if the score is closer to 1 and closer to 0 if unsimilar. RMSE and MAE scores of 0.071 and 0.0498 are achieved 
respectively.

To run the code:
```
python metrics.py
```

## Top-N recommendations single user

Choose user-id (uid - Surprise package) and run top_n_single_user.py, chooses the top n most similar tracks to the users previously listened to tracks.

To run the code:
```
python top_n_single_user.py
```
