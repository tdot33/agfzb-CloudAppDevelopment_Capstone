from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['psw']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            # login user and redirect to index page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "Oops! Something went wrong. Try again."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/4737848c-a6ec-49f3-88fd-9167ca9b806b/dealership-package/get-dealership.json"
        
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        # Add dealerships list to context
        context = {"dealerships": dealerships}

        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        
        # Return a list of dealer short name
        return render(request,'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/4737848c-a6ec-49f3-88fd-9167ca9b806b/dealership-package/get-review.json"
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        context = {"reviews": reviews, "dealer_id": dealer_id}
        print(context)
        # Construct a string with reviewer names and sentiments
        review_text = ""
        for review in reviews:
            review_text += f"Name: {review.name}, Sentiment: {review.sentiment}\n"

        # Return the review data as an HTTP response
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
@login_required
def add_review(request, dealer_id):
    if request.method == "POST":
        name = request.POST['name']
        dealership = request.POST['dealership']
        review_text = request.POST['review']
        purchase = request.POST['purchase']
        
        review = {
            "time": datetime.utcnow().isoformat(),
            "name": name,
            "dealership": dealership,
            "review": review_text,
            "purchase": purchase
        }

        json_payload = {
            "review": review
        }
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/4737848c-a6ec-49f3-88fd-9167ca9b806b/dealership-package/post-review"
        submit_review = post_request(url, json_payload, dealerId=dealer_id)

        return HttpResponse(submit_review, content_type="text/plain")