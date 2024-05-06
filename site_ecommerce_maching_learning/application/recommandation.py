import pandas as pd
from .models import ProductReview
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split
from surprise import KNNBasic, KNNWithMeans, KNNWithZScore, KNNBaseline, CoClustering, SVD








def get_recommendations1(algo, trainset, user_raw_id, n_recommendations):
        # Convert raw user ID to internal ID
        user_inner_id = trainset.to_inner_uid(user_raw_id)

        # Get all rated items for this user
        rated_items = set(x for x in trainset.ur[user_inner_id])
        #print(rated_items)
        # Create a list of all item IDs
        all_items = set(trainset.to_raw_iid(x) for x in range(trainset.n_items))

        # Get unrated items
        unrated_items = all_items - rated_items
        # Predict ratings for unrated items
        predictions = []
        for item in unrated_items:
            prediction = algo.predict(user_raw_id, item)
            predictions.append(prediction)
        # Sort predictions based on estimated rating
        predictions.sort(key=lambda x: x.est, reverse=True)

        # Return the top N recommendations
        return predictions[:n_recommendations]  # Return the top N recommendations as a list of tuples





def get_recommandation(data, user_raw_id, nm_comm):

    # Load data into Surprise Dataset
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(data[['User_ID', 'Product_ID', 'Rating']], reader)

    # Split the data into train and test sets (not necessary for generating recommendations)
    trainset, testset = train_test_split(dataset, test_size=0.2, random_state=42)
    predictions =[]
    # Use user_based true/false to switch between user-based or item-based collaborative filtering
    algo = KNNWithMeans(k=5, sim_options={'name': 'pearson_baseline', 'user_based': False})
    algo1 = KNNBasic(k=5, sim_options={'name': 'pearson_baseline', 'user_based': False})
    algo2 = KNNBaseline(k=5, sim_options={'name': 'pearson_baseline', 'user_based': False})
    algo3 = KNNWithZScore(k=5, sim_options={'name': 'pearson_baseline', 'user_based': False})
    algo4 = SVD()
    algo5 = CoClustering()
    score = [algo, algo1, algo2, algo3, algo4, algo5]
    #algo.fit(trainset)
    # SVD
    for alg in score:
        alg.fit(trainset)
        alg.test(testset)
        test_pred=alg.test(testset)
        predictions.append(accuracy.rmse(test_pred ,verbose=True))
        #make prediction using testset
        #print(predictions)
    #print RMSE
    #print("Item-based Model : Test Set")
    # Then compute RMSE
    #accuracy.rmse(predictions)

    minValue = min(predictions)
    index = predictions.index(minValue)
    print(index)
    alg = score[index]
    

    # Function to get recommended items for a specific user
    

    recommendations = get_recommendations1(alg, trainset, user_raw_id, nm_comm)

    return recommendations