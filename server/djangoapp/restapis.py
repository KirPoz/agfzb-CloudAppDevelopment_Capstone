import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

#APIKEY_LT = os.environ.get('APIKEY_LT_ENV', "not found")
#URL_LT = os.environ.get('URL_LT_ENV', "not found")
APIKEY_LT = ''
URL_LT = ''
VERSION_LT='2021-08-01'




# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    print(f"{json_payload}")
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, params=kwargs ,json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    print(f"With status {response.status_code}")
    print(f"Response: {response.text}")
    

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
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# get_dealers_by_state
def get_dealers_by_state(url=None, state=None):
    results = []
    # Call get_request with a URL parameter
    #url = url + state
    json_result = get_request(url, state=state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# get_dealers_by_id
def get_dealers_by_id(url=None, dealerId=None):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
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
def get_dealer_reviews_from_cf(url=None, dealerId=None):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Extracting values from json
            try: car_make = dealer_doc["car_make"]
            except Exception: car_make = "None"
            try: car_model = dealer_doc["car_model"]
            except Exception: car_model = "None"
            try: car_year = dealer_doc["car_year"]
            except Exception: car_year = "None"
            try: dealership = dealer_doc["dealership"]
            except Exception: dealership = "None"
            try: id = dealer_doc["id"]
            except Exception: id = "None"
            try: name = dealer_doc["name"]
            except Exception: name = "None"
            try: purchase = dealer_doc["purchase"]
            except Exception: purchase = "None"
            try: purchase_date = dealer_doc["purchase_date"]
            except Exception: purchase_date = "None"
            try: review = dealer_doc["review"]
            except Exception: review = "None"
            # Create a CarDealer object with values in `doc` object
            dealer_obj = DealerReview(car_make=car_make, car_model=car_model, car_year=car_year,
                                   dealership=dealership, id=id, name=name,
                                   purchase=purchase,
                                   purchase_date=purchase_date, review=review)
            dealer_obj.sentiment = analyze_review_sentiments(dealer_obj.review)
            results.append(dealer_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text=None):
    # Authentication
    authenticator = IAMAuthenticator(APIKEY_LT)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version=VERSION_LT,
        authenticator=authenticator)

    natural_language_understanding.set_service_url(URL_LT)
    try: 
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(
                keywords=KeywordsOptions(emotion=True, sentiment=True, limit = 1)
                ),
            language = 'en').get_result()
        return response['keywords'][0]['sentiment']['label']
    except:
        print("Network exception occurred")   
    

    








