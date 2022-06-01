from datetime import datetime
from pickle import TRUE
from sqlite3 import Date
from time import time
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.authentication import get_user_model

# 3rd party imports 
import uuid

#// location field 
class LocationModel(models.Model):
      
      lat = models.DecimalField(max_digits=30, 
                                decimal_places=20, 
                                null=True, blank=True)
      
      lng = models.DecimalField(max_digits=30, 
                                 decimal_places=20, 
                                 null=True, blank=True)
      
      primary_text = models.TextField(max_length= 100, 
                                       blank= True, null= True)
      
      secondary_text = models.TextField(max_length= 100, 
                                       blank= True, null= True)
      
      created_at = models.DateTimeField(auto_now_add= True)

#// booking Field 
class Booking(models.Model):

    # create fields 
    pickup_date = models.DateField(null = True)
    pickup_time = models.TimeField(null = True)
    
      # driver assigned to booking 
    booker = models.ForeignKey(get_user_model(), 
                                        on_delete=models.CASCADE,
                                        related_name=_('booker'), 
                                        null=True)
    
    assigned_driver = models.ForeignKey(get_user_model(), 
                                        on_delete=models.SET_NULL,
                                        null=True, 
                                        blank=True)
    
    additional_helpers = models.IntegerField(default = 0, null = True, blank = True)
    carry_floor = models.IntegerField(default = 0, null = True, blank = True)
    vehicle_type = models.FloatField(default = 1.0, null = True, blank = True)
    payment_option = models.CharField(default = 'CASH', max_length = 50, null=True, blank=True)
    drivers_note = models.TextField(default= 'No note left', max_length = 1000, null = True, blank = True)
    driver_rating = models.IntegerField(default = 0, blank = True)
    quote_price = models.FloatField(default = 1.0, null = True, blank = True)
    distance_km = models.FloatField(default = 0.0, null = True, blank = True)
    
    routes = models.ManyToManyField(LocationModel, blank = True)
 
    # whether the booking is completed or not 
    booking_completed = models.BooleanField(default=False, 
                                            null = False, blank=False)
    
    booking_cancelled = models.BooleanField(default=False, 
                                            null = False, blank=False)
    
    
    # created at 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # overide the string method 
    def __str__(self):
      
        return 'Booking uuid: {0}'.format(self.id)
      


    
    
    
    
    
    

