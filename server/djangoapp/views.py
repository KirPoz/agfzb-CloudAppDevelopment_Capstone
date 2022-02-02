from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealers_by_state, get_dealers_by_id, post_request
from .models import CarDealer, CarMake, CarModel
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

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
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to home page 
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
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
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
#def get_dealerships(request):
#    context = {}
#    if request.method == "GET":
#        return render(request, 'djangoapp/index.html', context)

# All dealer
#def get_dealerships(request):
#    context = {}
#    if request.method == "GET":
#        url = "https://164cb19c.eu-gb.apigw.appdomain.cloud/api/dealership"
#        # Get dealers from the URL
#        dealerships = get_dealers_from_cf(url)
#        # Concat all dealer's short name
#        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
#        # Return a list of dealer short name
#        return HttpResponse(dealer_names)

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://164cb19c.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealership_list = get_dealers_from_cf(url)
        # Get dealers
        context = {
            'dealership_list':dealership_list
        }
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# State 
#def get_dealerships(request):
#    if request.method == "GET":
#        url = "https://164cb19c.eu-gb.apigw.appdomain.cloud/api/dealership"
#        state = "CA"
#        # Get dealers from the URL
#        dealerships_by_state = get_dealers_by_state(url = url, state = state)
#        # Concat all dealer's short name
#        dealer_names = ' '.join([dealer.short_name for dealer in dealerships_by_state])
#        # Return a list of dealer short name
#        return HttpResponse(dealer_names)

# dealerId
#def get_dealerships(request):
#    if request.method == "GET":
#        url = "https://164cb19c.eu-gb.apigw.appdomain.cloud/api/dealership"
#        dealerId = '1'
#        # Get dealers from the URL
#        dealerships_by_id = get_dealers_by_id(url = url, dealerId = dealerId)
#        # Concat all dealer's short name
#        dealer_names = ' '.join([dealer.short_name for dealer in dealerships_by_id])
#        # Return a list of dealer short name
#        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
#def get_dealer_details(request, dealer_id=None):
#    if request.method == "GET":
#        url = "https://164cb19c.eu-gb.apigw.appdomain.cloud/api/review"
#        # Get dealers from the URL
#        dealer_details_by_id = get_dealer_reviews_from_cf(url = url, dealerId = dealer_id)
#        # Concat all dealer's short name
#        dealer_review = ' '.join([dealer.review for dealer in dealer_details_by_id])
#        dealer_sentiment = ' '.join([dealer.sentiment for dealer in dealer_details_by_id])
#        # Return a list of dealer short name
#        return HttpResponse(dealer_review + dealer_sentiment)
#        #return render(request, 'djangoapp/dealer_details.html', context)

def get_dealer_details(request, dealer_id=None):
    context = {}
    if request.method == "GET":
        url_review = "https://164cb19c.eu-gb.apigw.appdomain.cloud/api/review"
        url_dealer = "https://164cb19c.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealer_details_list = get_dealer_reviews_from_cf(url = url_review, dealerId = dealer_id)
        dealerships_info = get_dealers_by_id(url = url_dealer, dealerId = dealer_id)
        # Get dealers review
        context = {
            'dealer_details_list':dealer_details_list,
            'dealerships_info':dealerships_info,
        }
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id=None):
    context = {}
    url_dealer = "https://164cb19c.eu-gb.apigw.appdomain.cloud/api/dealership"
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        dealerships_info = get_dealers_by_id(url = url_dealer, dealerId = dealer_id)
        cars = CarModel.objects.all().filter(dealer_id = dealer_id)
        context = {
            "dealer_id": dealer_id,
            'dealerships_info': dealerships_info,
            "cars": cars,
        }
        return render(request, 'djangoapp/add_review.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user object
        user = request.user
        # Check Authentication
        if user.is_authenticated:
            car = CarModel.objects.get(pk=request.POST['car'])
            review ={
                #"id" = dealer_id
                "name": request.user.username,
                "review": request.POST['content'],
                "dealership": dealer_id,
                "purchase": request.POST.get("purchasecheck"),
                "purchase_date": datetime.strptime(request.POST['purchasedate'], "%m/%d/%Y").isoformat(),
                #datetime.utcnow().isoformat() datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                "car": car.car_name,
                "car_make": car.car_make.car_name,
                "car_year": car.car_year.strftime("%Y"),
            }

            #json_payload["review"] = review
            print(f"{review}")

            url = "https://164cb19c.eu-gb.apigw.appdomain.cloud/api/dealership/review"
            #post_request(url, json_payload, dealerId=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            # Redirect to show_exam_result with the submission id
            return redirect('djangoapp:login')





