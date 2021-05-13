
from collections import defaultdict

from surprise import Dataset, Reader

from content_knn import ContentKNN
from tracks_data import convert_track_id_names


RATINGS_FILEPATH = './data/ratings_data.csv'


def generate_anti_test_set_for_user(full_trainset, uid=1004584):
    """
    Builds a testset of the tracks the user hasn't listened to yet so they
    are not recommeded'
    """
    u = full_trainset.to_inner_uid(str(uid))
    fill = full_trainset.global_mean
    user_tracks = set([j for (j, _) in full_trainset.ur[u]])
    anti_testset = [(full_trainset.to_raw_uid(u), full_trainset.to_raw_iid(i), fill) for
                     i in full_trainset.all_items() if
                     i not in user_tracks]
    return anti_testset


def get_top_n(predictions, n=10):
    # Map the predictions of each user
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))
    
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
        
    return top_n


if __name__ == "__main__":
    
    # define ratings dataset and load
    reader = Reader(line_format='user item rating timestamp', sep=',', rating_scale=(0.0, 1.0), skip_lines=1)
    ratings_dataset = Dataset.load_from_file(RATINGS_FILEPATH, reader=reader)
    
    #pdb.set_trace()
    
    # find track names from track uris
    track_uri_to_name = convert_track_id_names()
    
    # build full training set/build anti testset
    trainset = ratings_dataset.build_full_trainset()
    testset = generate_anti_test_set_for_user(trainset)
    
    # create content knn object
    c_knn = ContentKNN()
    c_knn.fit(trainset)
        
    predictions = c_knn.test(testset)
    
    top_n = get_top_n(predictions)
    
    # print the recommended tracks for each user
    for uid, user_ratings in top_n.items():
        print(f"The top-{len(user_ratings)} recommendations for user-{uid} are: ")
        print(uid, [(track_uri_to_name[iid], est) for (iid, est) in user_ratings])
    