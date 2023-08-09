from django.db import models
from django.utils.timezone import now

# Create your models here.

# CarMake model
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Generic')
    description = models.CharField(null=False, max_length=50, default='Standard')
    def __str__(self):
        return self.name

# CarModel model
class CarModel(models.Model):
    name = models.CharField(null=False, max_length=30, default="Car")
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    SEDAN = "sedan"
    SUV = "SUV"
    WAGON = "wagon)"
    type_choices = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon")
    ]
    car_type = models.CharField(null=False, max_length=20, choices=type_choices, default=SEDAN)
    year = models.DateField()
    def __str__(self):
        return self.name

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

    def __init__(name, dealership, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        # Reviewer name
        self.name = name
        # Dealership
        self.dealership = dealership
        # Purchase status
        self.purchase = purchase
        # Purchase date
        self.purchase_date = purchase_date
        # Car Make
        self.car_make = car_make
        # Car Model
        self.car_model = car_model
        # Car Year
        self.car_year = car_year
        # Review
        self.revew = review
        # Review sentiment
        self.sentiment = sentiment
        # Review ID
        self.id = id

    def __str__(self):
        return "Review ID: " + self.id