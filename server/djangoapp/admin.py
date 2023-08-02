from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 0

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['name','dealer_id']

admin.site.register(CarModel, CarModelAdmin)

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name','description']
    inlines = [CarModelInline]

admin.site.register(CarMake, CarMakeAdmin)
