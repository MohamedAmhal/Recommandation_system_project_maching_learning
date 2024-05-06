import pickle
import json
from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
from surprise import Dataset
from surprise import Reader





electronics_data = pd.read_csv('ratings_Electronics.csv', names=['userId', 'productId','rating','timestamp'])

electronics_data.drop('timestamp', axis=1, inplace=True)


reader = Reader(rating_scale=(1, 5))
data = electronics_data.groupby('productId').filter(lambda x:x['rating'].count()>=50)
surprise_data = Dataset.load_from_df(data,reader)




app = FastAPI()


class model_input(BaseModel):

    userID      : str



KNNsurpriseModel = pickle.load(open('KNNsurprise.sva', 'rb'))



@app.post('/item_based_recommendation')
def item_pred(input_parameters : model_input):

    input_data = input_parameters.json()
    input_dictionnary = json.loads(input_data)
    
    user_ID = input_dictionnary['userID']



    # Get all unique item IDs in the dataset that are not rated by the specified user
    all_item_ids = set(iid for uid, iid, _, _ in surprise_data.raw_ratings if uid != user_ID)

    # Make predictions for all items for the specified user
    predictions = [KNNsurpriseModel.predict(user_ID, item_id) for item_id in all_item_ids]

    # I added this to get only the top 50 products
    sorted_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)[:50]

    
    """ # Print predictions
    for prediction in sorted_predictions:
        print(f"Predicted rating for user {user_ID} on item {prediction.iid}: {prediction.est}") """

    


    # We can later store the products id we want then transfer them to website for them to be shown
    recommended_products = [(prediction.iid, prediction.est) for prediction in sorted_predictions]


    return recommended_products