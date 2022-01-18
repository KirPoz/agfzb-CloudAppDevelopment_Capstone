
import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()
from django.conf import settings


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    care_name = models.CharField(max_length=1000)
    car_description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.car_name + "," + \
               "Description: " + self.car_description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    care_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    care_name = models.CharField(max_length=1000)
    dealer_id = models.IntegerField(null=False)
    SEDAN = 'sedan'
    SUS = 'sus'
    WAGON = 'wagon'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUS, 'SUS'),
        (WAGON, 'WAGON')
    ]
    care_type = models.CharField(
        null=False,
        max_length=50,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    car_year = models.DateField(null=False)

    def __str__(self):
        return "Name: " + self.car_name




# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
