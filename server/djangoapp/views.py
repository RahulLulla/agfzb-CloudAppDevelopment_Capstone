from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel,CarDealer,CarMake
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import random
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
        dealerships = get_dealers_from_cf(url)
        context = { 'dealership_list':dealerships }
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # dealer_st = ' '.join([dealer.st for dealer in dealerships])
        # Return a list of dealer short name
        # return HttpResponse('Dealer names: ' + dealer_names +'Short Names: '+dealer_st)
        return render(request, 'djangoapp/index.html', context)

def get_dealerships_by_state(request, state):
    if request.method == "GET":
        url = "https://1f0aa1ef.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_by_state(url,state=state)
        context = { 'dealership_list':dealerships }
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # dealer_st = ' '.join([dealer.st for dealer in dealerships])
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        # Get all reviews for dealer ID
        url = "https://1f0aa1ef.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url,dealerId=dealer_id)
        # Get all dealership name for dealer ID
        url = "https://1f0aa1ef.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships_name = get_dealer_name_by_ID(url,dealer_id)
        # review_list = ' '.join([r.review for r in reviews])
        # return HttpResponse(review_list)
        return render(request, 'djangoapp/dealer_details.html', {'reviews_obj_list': reviews,
        'dealerships_name':dealerships_name,
        'dealer_id':dealer_id})

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        cars = {}
        json_payload = {}
        print("User is logged in :)")
        print(f"Username --> {request.user.username}")
        if request.method == "GET":
            # querying the cars with the dealer id to be reviewed
            url = "https://1f0aa1ef.us-south.apigw.appdomain.cloud/api/dealership"
            dealerships_name = get_dealer_name_by_ID(url,dealer_id)
            result = CarModel.objects.filter(dealer_id=dealer_id)#.values_list( flat=True)
            return render(request, 'djangoapp/add_review.html', 
            {'cars': result,'dealerships_name':dealerships_name,
            'dealer_id':dealer_id})
        else:
            url = "https://1f0aa1ef.us-south.apigw.appdomain.cloud/api/review"
            review = {}
            if "purchase_date" in request.POST:
                purchase_datetime = datetime.strptime(request.POST['purchasedate'], '%m/%d/%Y')#%H:%M:S.%f
                review["purchase_date"] = purchase_datetime.isoformat(timespec='milliseconds')
                review["purchase_date"] = json.dumps(review["purchase_date"], default=str)
            else:
                review["purchase_date"] = ''
            review["dealership"] = dealer_id
            review["review"] = request.POST['reviewContent']
            review["name"] = request.user.username
            review["purchase"] = True if 'purchasecheck' in request.POST else False
            review["id"] = random.randint(101,1000)
            review["another"] = "field"
            print('purchasedate',review["purchase_date"])
            print('datetime.utcnow().isoformat():',datetime.utcnow().isoformat())
            car = CarModel.objects.get(pk=int(request.POST['car']))
            print(car.carmake.name,car.name,car.year)
            review["car_make"] = car.carmake.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
            json_payload["review"] = review
            status_code = post_request(url, json_payload, 
                                        dealerId=dealer_id)
            # After post we would see list of reviews for the dealerid updated
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        print("User is not logged in :(")
    return HttpResponse("Error code: 500 User is not logged in :(")
    
