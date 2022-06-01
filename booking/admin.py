from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# local imports 
from .models import Booking, LocationModel


# register model to site 
admin.site.register(Booking)
admin.site.register(LocationModel)