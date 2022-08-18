from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def service(request):
    context = {}
    return render(request, 'djangoapp/service.html', context)
    
# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    if request.method == "GET":
        # url = "https://1f0aa1ef.us-south.apigw.appdomain.cloud/api/dealership?state=\"Texas\""
        url = "https://1f0aa1ef.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        # dealerships = get_dealers_from_cf(url)
        dealerships = get_dealers_by_state(url,state="California")
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        #dealer_st = ' '.join([dealer.st for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names) #+'\n'+dealer_st)

def get_dealerships_by_state(request, state):
    if request.method == "GET":
        url = "https://1f0aa1ef.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_by_state(url,state=state)
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        dealer_st = ' '.join([dealer.st for dealer in dealerships])
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://1f0aa1ef.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url,dealerId=dealer_id)
        list_review = ' '.join([r.review for r in reviews])
        return HttpResponse(list_review)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    review = {}
    json_payload = {}
    url = "https://1f0aa1ef.us-south.apigw.appdomain.cloud/api/review"
    if request.user.is_authenticated:
        print("User is logged in :)")
        print(f"Username --> {request.user.username}")
        review["purchase_date"] = datetime.utcnow().isoformat()
        review["dealership"] = dealer_id
        review["review"] = "This is a great car dealer"
        review["name"] = "Sam L Jackson"
        review["purchase"] = True
        review["car_make"] = "Pontiac"
        review["car_model"] = "Firebird"
        review["car_year"] = 1995
        review["id"] = 101
        review["another"] = "field"
        json_payload["review"] = review
        status_code = post_request(url, json_payload, dealerId=dealer_id)
    else:
        print("User is not logged in :(")
        status_code = 500
    return HttpResponse(status_code)

