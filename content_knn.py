import numpy as np

from surprise import AlgoBase
from surprise import PredictionImpossible

from tracks_data import get_audio_features, get_genres


class ContentKNN(AlgoBase):
    
    def __init__(self, k=10):
        AlgoBase.__init__(self)
        self.k = k
        
    def fit(self, trainset):
        AlgoBase.fit(self, trainset)
        
        audio_features = get_audio_features()
        genres = get_genres()
        
        print('Creating similarity matrix')
        
        # create similarity matrix 
        self.sim_matrix = np.zeros((self.trainset.n_items, self.trainset.n_items))
        
        for outer_track in range(self.trainset.n_items):
            print(outer_track, self.trainset.n_items)
            outer_track_id = self.trainset.to_raw_iid(outer_track)
            for inner_track in range(outer_track + 1, self.trainset.n_items):
                inner_track_id = self.trainset.to_raw_iid(inner_track)
                """
                #GENRES
                genres_similarity = self.cosine_similarity(outer_track_id, inner_track_id, genres)
                self.sim_matrix[outer_track, inner_track] = genres_similarity
                self.sim_matrix[inner_track, outer_track] = genres_similarity
                """
                """
                #AUDIO FEATURES + GENRES
                audio_features_similarity = self.cosine_similarity(outer_track_id, inner_track_id, audio_features)
                genres_similarity = self.cosine_similarity(outer_track_id, inner_track_id, genres)
                sim = audio_features_similarity * genres_similarity
                self.sim_matrix[outer_track, inner_track] = sim
                self.sim_matrix[inner_track, outer_track] = sim
                """
              
                audio_features_similarity = self.cosine_similarity(outer_track_id, inner_track_id, audio_features)
                self.sim_matrix[outer_track, inner_track] = audio_features_similarity
                self.sim_matrix[inner_track, outer_track] = audio_features_similarity
                
        print('Finished creating similarity matrix')
        
        return self
    
    def cosine_similarity(self, track1, track2, feature):
        track1_feature = feature[track1]
        track2_feature = feature[track2]
        total_x, total_y, total_xy = 0, 0, 0
        for i in range(len(track1_feature)):
            total_x += track1_feature[i] * track1_feature[i]
            total_y += track2_feature[i] * track2_feature[i]
            total_xy += track1_feature[i] * track2_feature[i]
        return total_xy / ((np.sqrt(total_x)) * (np.sqrt(total_y)))
    
    def estimate(self, u, i):
        if not(self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            raise PredictionImpossible('User and/or item is unknown.')
        
        # Compute similarities between the test track and all of the tracks
        # the user has listened to
        neighbours = sorted([self.sim_matrix[track_id, i] for track_id, rating \
                             in self.trainset.ur[u]], reverse=True)[:self.k]
            
        total_sim = sum(neighbours)
        
        if total_sim == 0:
            raise PredictionImpossible('There are no neighbours for this track!')
            
        pred_rating = total_sim / len(neighbours)
        
        return pred_rating
    