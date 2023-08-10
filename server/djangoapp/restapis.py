import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests

import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, api_key=None, params=None, **kwargs):
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

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["documents"]
        print(json_result)
        # Create DealerReview object with values from the reviews dict
        for review in reviews:
            review_obj = DealerReview(
                name=review["name"],
                dealership=review["dealership"],
                purchase=review["purchase"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                review=review["review"],
                id=review["id"],
                sentiment=analyze_review_sentiments(review["review"])          
            )
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    results = []
    # - Call get_request() with specified arguments
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/ecbd1545-b8fb-4bcb-bd20-24cb98b6d7d7"
    apikey = "zbnqBLYHFy9sQAfOwfFs2oy6KNDXj90j_TBQZrdIsjTo"
    params = {
        "text": text,
        "version": "2021-09-01",
        "features": "sentiment",
        "return_analyzed_text": True
    }
    
    response = requests.get(
        url,
        params=params,
        headers=headers,
        auth=HTTPBasicAuth('apikey', api_key)
    )

    if response.status_code == 200:
        sentiment = response.json()["sentiment"]["document"]["label"]
        return sentiment
    else:
        print("Sentiment analysis failed with status code:", response.status_code)

    return None
    # - Get the returned sentiment label such as Positive or Negative



