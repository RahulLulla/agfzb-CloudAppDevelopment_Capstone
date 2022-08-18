import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, SentimentOptions
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('api_key')
nlu_watson_url = os.getenv('nlu_watson_url')

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    # print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, params=kwargs, 
                headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, 
                headers={'Content-Type': 'application/json'},
                params=kwargs)                                    
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        # print(json_result)
        dealers = json_result["result"]
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealers_by_state(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,state=kwargs["state"])
    if json_result and "result" in json_result:
        # Get the row list in JSON as dealers
        # print(json_result)
        dealers = json_result["result"]
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results    

# get_dealer_reviews_from_cf to get all reviews by dealer's id.
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,dealerId=kwargs["dealerId"])
    if json_result and "result" in json_result:
        # Get the row list in JSON as dealers
        # print(json_result)
        reviews = json_result["result"]
        # For each dealer object
        for review_doc in reviews:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"],
                name=review_doc["name"],
                purchase=review_doc["purchase"],
                review=review_doc["review"],
                purchase_date=review_doc["purchase_date"],
                car_make=review_doc["car_make"],
                car_model=review_doc["car_model"],
                car_year=review_doc["car_year"],
                id=review_doc["id"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
            print('Review:',review_obj.review)
            print('Sentiment:',review_obj.sentiment)
            # print(str(review_obj))

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    params = dict()
    params["return_analyzed_text"]=True
    params["text"] = dealerreview
    params["version"] = '2019-07-12'
    params["features"] = {"keywords":{"sentiment": True,"limit": 1}}
    '''
    https://github.com/RahulLulla/cazgi-IBM-Watson-NLU-Project/blob/master/sentimentAnalyzeServer/sentimentAnalyzerServer.js
            {
            "text": textToAnalyze,
            "features": {
                "keywords": {
                    "sentiment": true,
                    "limit": 1
                }
            }
        }
    '''
    try:
        response = requests.get(nlu_watson_url, params=params, 
            headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth('apikey', api_key))
        status_code = response.status_code
        print("Analysis request status code {} ".format(status_code))
        json_data = json.loads(response.text)
        print('response: ',response)
        print(json_data)
        return json_data
    except Exception as e:
        print("Network exception occurred")
        print(e)

    # status_code = response.status_code
    # print("With status {} ".format(status_code))
    # json_data = json.loads(response.text)
    # print(json_data)
    return {}


def post_request(url, json_payload, **kwargs):
    # try:
    #     response = requests.post(url, params=kwargs, json=json_payload)
    # except Exception as e:
    #     print(e)    

    response = requests.post(url, params=kwargs, json=json_payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    # json_data = json.loads(response.text)
    return status_code