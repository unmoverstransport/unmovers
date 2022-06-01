
# third party imports 

from rest_framework import serializers
from rest_framework.reverse import reverse
from accounts.models import NewUser, UserProfile
from accounts.serializers import BookingUserProfileSerializer

# app imports 
from .models import Booking 
import googlemaps


""" 
request = self.context.get('request)
if request is none:
    return None 
return reverse("update-booking", kwargs={"pk": obj.pk}, request = request)
"""

# create booking serializer 
class BookingSerializer(serializers.ModelSerializer):
    
    # here we can add additional fields 
    booker = serializers.SerializerMethodField(read_only = True)
    edit_url = serializers.SerializerMethodField(read_only = True)
    delete_url = serializers.SerializerMethodField(read_only = True)
    retrieve_url = serializers.SerializerMethodField(read_only = True)
    assigned_driver = serializers.SerializerMethodField(read_only = True)
    locations = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Booking
        fields = [
        
            'id',
            'pickup_date',
            'pickup_time',
            'quote_price',
            'distance_km',
            'retrieve_url',
            'edit_url',
            'delete_url',
            'booker',
            'assigned_driver', 
            'additional_helpers',
            'drivers_note',
            'carry_floor',
            'payment_option',
            'locations',
            'vehicle_type',
            'driver_rating',
            'booking_completed',
            'booking_cancelled',
            'created_at',
            
        ]
        
    def get_locations(self, obj):
        
        #// list containing latlong primary and secondary texts 
        _locations = [];
    
        
        if len(obj.routes.all())  == 0: return _locations;
            
        #// loop 
        for _location in obj.routes.all():
                    
            #// placeholder for locations model
            payload = dict()
            #lat_long_list.append([item.lat, item.lng])
            payload['lat'] = _location.lat
            payload['lng'] = _location.lng
            payload['primary_text'] = _location.primary_text
            payload['secondary_text'] = _location.secondary_text
            
            #print(_location.lat, _location.lng)
            
            #// append 
            _locations.append(payload)

        return _locations   
        
    def get_edit_url(self, obj):
        request = self.context.get('request') or None 
        if request is None:
            return None 
        return reverse('update-booking', 
                       kwargs={"pk": obj.pk},
                       request=request)
        
    def get_retrieve_url(self, obj):
        request = self.context.get('request') or None 
        if request is None:
            return None 
        return reverse('retrieve-booking', 
                       kwargs={"pk": obj.pk},
                       request=request)
    
    def get_delete_url(self, obj):
        request = self.context.get('request') or None 
        if request is None:
            return None 
        return reverse('delete-booking', 
                       kwargs={"pk": obj.pk}, 
                       request=request)
        
    def get_booker(self, obj):
        
        request = self.context.get('request') or None 
        
        if not isinstance(obj.booker, NewUser): return None 
        if obj.booker is None: return None 
        # otherwise
        user_p = UserProfile.objects.get(user = obj.booker) or None 
        if user_p is None: return {"error_msg": "user doesnt exist"}
        
        #// set payload 
        payload = {'request': request}
    
        # otherwise
        user_full_p = BookingUserProfileSerializer(user_p,
                                                context = payload, 
                                                many = False)
        return user_full_p.data
    
    
    def get_assigned_driver(self, obj):
        
        request = self.context.get('request') or None 

        if not isinstance(obj.assigned_driver, NewUser): return None 
        if obj.assigned_driver is None: return None 
        # otherwise
        user_p = UserProfile.objects.get(user = obj.assigned_driver) or None 
        if user_p is None: return {"error_msg": "user doesnt exist"}
        
        #// set payload 
        payload = {'request': request}
    
        # otherwise
        user_full_p = BookingUserProfileSerializer(user_p, context = payload, many = False)
        return user_full_p.data
          


#// here we need to write a view that will calculate the distance for us 
