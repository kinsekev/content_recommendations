
from surprise import Reader, Dataset
from surprise.model_selection import train_test_split, cross_validate
from surprise import accuracy
from content_knn import ContentKNN
import os


RATINGS_FILEPATH = './data/ratings_data.csv'


if __name__ == "__main__":
    
    # define ratings dataset and load
    reader = Reader(line_format='user item rating timestamp', sep=',', rating_scale=(0.0, 1.0), skip_lines=1)
    ratings_dataset = Dataset.load_from_file(RATINGS_FILEPATH, reader=reader)

    # create content knn object
    c_knn = ContentKNN()
    
    cross_validate(c_knn, ratings_dataset, measures=['RMSE', 'MAE'], cv=3, verbose=True)
    
    
    