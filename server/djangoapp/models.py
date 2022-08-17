from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=30, default='Name')
    description = models.CharField(null=False, max_length=60, default='Description')

    def __str__(self):
        return self.name + "," + \
               self.description
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    id = models.AutoField(primary_key=True)
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='Name')
    dealer_id = models.IntegerField(default=0)
    year = models.DateField(null=True)
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    CAR_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]
    car_type = models.CharField(
        null=False,
        max_length=20,
        choices=CAR_CHOICES,
        default=SEDAN
    )

    def __str__(self):
        return str(self.dealer_id) + "," + \
                self.name + "," + \
                self.car_type + "," + \
                str(self.year) + "," + \
               self.carmake.name + "," + \
               self.carmake.description

# <HINT> Create a plain Python class `CarDealer` to hold dealer data

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership,name,purchase,review,purchase_date,car_make,car_model,car_year,id):
        self.id = id
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        POSITIVE = 'positive'
        NEUTRAL = 'neutral'
        NEGATIVE = 'negative'
        SENTIMENT_CHOICES = [
            (POSITIVE, 'positive'),
            (NEUTRAL, 'neutral'),
            (NEGATIVE, 'negative'),
        ]                
        self.sentiment = models.CharField(
        null=False,
        max_length=20,
        choices=SENTIMENT_CHOICES
        )        

    def __str__(self):
        return "Dealership name: " + self.dealership \
        + "Name: " + self.name
