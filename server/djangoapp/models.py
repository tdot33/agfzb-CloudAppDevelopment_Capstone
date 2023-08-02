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


# <HINT> Create a plain Python class `DealerReview` to hold review data
