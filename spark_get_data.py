"""
run gen_users first on single cloud
check what type fields are in users, artists, albums, tracks - leverage listening events
change file paths for reading/writing files
"""

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('LFM').getOrCreate()

########################################################################################################################
"""
Users
user-id, country, age, gender, playcount, registered timestamp
"""

users = spark.read.option("header", "true") \
    .option("delimiter", "\t") \
    .option("inferSchema", "true") \
    .csv('./LFM-1b_users.txt')

users = users.drop('registered_unixtime')
users = users.dropna(how='any')
users = users.filter((users['age'] != -1) & (users['gender'] != 'n'))
users = users.filter(users['playcount'] > 40649)


c = 1.0*200 / users.count()
users = users.sample(withReplacement=False, fraction=c)

print('Loaded Users..')

########################################################################################################################
"""
artists
artist-id, artist-name
"""

artists = spark.read.option("header", "true") \
    .option("delimiter", "\t") \
    .option("inferSchema", "true") \
    .csv('./LFM-1b_artists.txt')


artists = artists.withColumnRenamed('0', 'artist_id')
artists = artists.withColumnRenamed('1', 'artist_name')
artists = artists.dropna(how='any')

print('Loaded artists')

########################################################################################################################
"""
albums
album-id, album-name, artist-id
"""

albums = spark.read.option("header", "true") \
    .option("delimiter", "\t") \
    .option("inferSchema", "true") \
    .csv('./LFM-1b_albums.txt')

albums = albums.withColumnRenamed('0', 'album_id')
albums = albums.withColumnRenamed('1', 'album_name')
albums = albums.withColumnRenamed('2', 'artist_id')
albums = albums.dropna(how='any')

print('Loaded albums')

########################################################################################################################
"""
tracks
track-id, track-name, artist-id
"""

tracks = spark.read.option("header", "true") \
    .option("delimiter", "\t") \
    .option("inferSchema", "true") \
    .csv('./LFM-1b_tracks.txt')

tracks = tracks.withColumnRenamed('0', 'track_id')
tracks = tracks.withColumnRenamed('1', 'track_name')
tracks = tracks.withColumnRenamed('2', 'artist_name')
tracks = tracks.dropna(how='any')

print('Loaded tracks')

########################################################################################################################
"""
LE's
user-id, artist-id, album-id, track-id, timestamp
"""

l_events = spark.read.option("header", "true") \
    .option("delimiter", "\t") \
    .option("inferSchema", "true") \
    .csv('./LFM-1b_LEs.txt')

l_events = l_events.withColumnRenamed('0', 'user_id')
l_events = l_events.withColumnRenamed('1', 'artist_id')
l_events = l_events.withColumnRenamed('3', 'album_id')
l_events = l_events.withColumnRenamed('4', 'track_id')
l_events = l_events.withColumnRenamed('5', 'timestamp')
l_events = l_events.dropna(how='any')

print('Listening Events')

########################################################################################################################

# join l_events with users
l_events = l_events.join(users, l_events.user_id == users.user_id, 'inner')\
                .select(l_events.user_id, l_events.artist_id, l_events.album_id, l_events.track_id, l_events.timestamp,
                        users.country, users.age, users.gender, users.playcount)
print('Joined listening events with users')

# join l_events with artists
l_events = l_events.join(artists, l_events.artist_id == artists.artist_id, 'inner')\
                .select(l_events.user_id, l_events.album_id, l_events.track_id, l_events.timestamp,
                        l_events.country, l_events.age, l_events.gender, l_events.playcount, artists.artist_name)
print('Joined listening events with artists')

# join l_events with albums
l_events = l_events.join(albums, l_events.album_id == albums.album_id, 'inner')\
                .select(l_events.user_id, l_events.track_id, l_events.timestamp, l_events.country, l_events.age,
                        l_events.gender, l_events.playcount, l_events.artist_name, albums.album_name)
print('Joined listening events with artists')

# join l_events with tracks
l_events = l_events.join(tracks, l_events.track_id == tracks.track_id, 'inner')\
                .select(l_events.user_id, l_events.timestamp, l_events.country, l_events.age, l_events.gender,
                        l_events.playcount, l_events.artist_name, l_events.album_name, tracks.track_name).collect()
print('Joined listening events with tracks')

# take sample from this frame
c = ((1.0*200) / users.count())
c = ((1.0*10000) / l_events.count())

# change fraction when found number of rows
print('selecting sample')
sub_l_events = l_events.sample(withReplacement=False, fraction=c)

# write csv
print('writing csv')
users.write.csv('./gen_data.csv', header=True)

print('finished')
