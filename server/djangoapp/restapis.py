import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

def get_request(url, api_key=None, params=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        headers = {'Content-Type': 'application/json'}
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(
                url, 
                params=params, 
                headers={'Content-Type': 'application/json'}, 
                auth=HTTPBasicAuth('apikey', api_key),
                **kwargs
            )
        else:
            response = requests.get(url, params=params, headers=headers, **kwargs)
        
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")
        return None

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    print("POST to {} ".format(url))
    try:
        response = requests.post(url, json=json_payload, **kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = response.json()
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")
        return None

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the "documents" array from the JSON response
        dealers = json_result["documents"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values from the dealer_doc dictionary
            dealer_obj = CarDealer(
                address=dealer["address"],
                city=dealer["city"],
                full_name=dealer["full_name"],
                id=dealer["id"],
                lat=dealer["lat"],
                long=dealer["long"],
                short_name=dealer["short_name"],
                state=dealer["state"],
                st=dealer["st"],
                zip=dealer["zip"]
            )
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # - Call get_request() with specified arguments
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the "documents" array from the JSON response
        dealers = json_result["documents"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values from the dealer_doc dictionary
            dealer_obj = CarDealer(
                address=dealer["address"],
                city=dealer["city"],
                full_name=dealer["full_name"],
                id=dealer["id"],
                lat=dealer["lat"],
                long=dealer["long"],
                short_name=dealer["short_name"],
                st=dealer["st"],
                zip=dealer["zip"]
            )
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function

def get_all_reviews_from_cf(url):
    json_result = get_request(url)
    if json_result:
        reviews = json_result["documents"]
        return reviews
    return []

def get_dealer_reviews_from_cf(url, dealerId):
    reviews = get_all_reviews_from_cf(url)
    filtered_reviews = [review for review in reviews if review["dealership"] == dealerId]
    results = []
    for review in filtered_reviews:
        review_sentiment = {
            "text": review["review"]
        }
        print(review_sentiment)
        sentiment = analyze_review_sentiments(review_sentiment)
        print(sentiment)  # Calculate sentiment
        review_obj = DealerReview(
            name=review["name"],
            dealership=review["dealership"],
            purchase=review["purchase"],
            purchase_date=review.get("purchase_date", ""),  # Use .get() to handle missing key
            car_make=review.get("car_make", ""),
            car_model=review.get("car_model", ""),
            car_year=review.get("car_year", ""),
            review=review["review"],
            sentiment=sentiment["sentiment"],  # Set sentiment directly
            id=review["id"]          
        )
        results.append(review_obj)
    
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    authenticator = IAMAuthenticator('zbnqBLYHFy9sQAfOwfFs2oy6KNDXj90j_TBQZrdIsjTo')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-08-10',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url('https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com')

    try:
        analyze_params = {
            'text': text['text'],
            'features': {
                'sentiment': {
                    'document': True
                }
            }
        }

        analysis_results = natural_language_understanding.analyze(**analyze_params).get_result()
        sentiment_label = analysis_results['sentiment']['document']['label']

        response = {
            'sentiment': sentiment_label
        }

        return response
    except Exception as error:
        print('Error:', error)