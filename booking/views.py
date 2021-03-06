
#from tokenize import Token

from django.shortcuts import get_object_or_404
from rest_framework import status
import json
from rest_framework.response import Response
from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
# Create your views here.
from .pagination import BookingsPaginator
from .models import Booking, LocationModel
from .serializers import BookingSerializer

from django.utils.translation import gettext_lazy as _
import googlemaps

#// we need the date time module 
from datetime import date, datetime

#// safe 
from decouple import config

"""
paginator = BookingsPaginator()
results = paginator.paginate_queryset(Posts)
serializer = PostsSerializer(results, many = true, context = {request:request})
return paginator.get_paginated_response(serializer.data)

Here we gonna use class based views 
"""
client = googlemaps.Client(key = config('GOOGLE_API_KEY', cast=str))


# this is to return all the bookings (STAFF VIEW) 
class CustomerBookingsListAPIView(generics.ListAPIView):
    
    # these have to be set by default 
    queryset = Booking.objects\
                        .all()\
                        .order_by('-created_at')
    serializer_class = BookingSerializer
    pagination_class = BookingsPaginator

    #authentication_classes = [JWTTokenUserAuthentication,]
    #permission_classes = [IsAuthenticated,]
     
# customer view bookings 
# here we gonna create get user bookings 
# create and get 
class CustomerViewOwnBookingsCreateAPIView(generics.CreateAPIView):
    
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated,]
    
    def post(self, request, *args, **kwargs):
        
        #// create payload 
        payload = {}
        _booking = None
        
        #// get the currently logged in user 
        loggedin_user = request.user
        
        #// request all parameters 
        pickup_date = request.data.get('pickup_date') or None 
        pickup_time = request.data.get('pickup_time') or None 
        quote_price = request.data.get('quote_price') or None
        mid_month_discount = request.data.get('mid_month_discount')
        loyal_customer_discount = request.data.get('loyal_customer_discount') 
        distance_km = request.data.get('distance')
        payment_option = request.data.get('payment_option') 
        carry_floor = request.data.get('carry_floor')  
        vehicle_type = request.data.get('vehicle_type') or None  
        drivers_note = request.data.get('drivers_note') 
        additional_helpers = request.data.get('additional_helpers') 
        booking_completed = request.data.get('booking_completed')
        booking_cancelled = request.data.get('booking_cancelled') 
        did_apply_loyal_discount = request.data.get('did_apply_loyal_discount')
        
        
        #// most importantly routes
        routes = request.data.get('routes') or None 
        
        if(loggedin_user is None):
            #// this means the token is invalid 
            errorPayload = dict()
            
            #// set error 
            errorPayload['error'] = 'Token is invalid or expired, please re-signin'
            errorPayload['status'] = status.HTTP_401_UNAUTHORIZED
            
            #// return response 
            return Response(errorPayload, status=status.HTTP_401_UNAUTHORIZED)

        #// check sent values are none or valid 
        if(routes is None or pickup_date is None or 
                        pickup_time is None or vehicle_type is None 
                                or quote_price is None or distance_km is None
                                    or mid_month_discount is None 
                                        or loyal_customer_discount is None):
            
            #set the payload and
            payload['error_message'] = 'booking routes|pickup|quote-price, date or pickup time cannot be null'
            # payload['error_message'] = message
            return Response(payload, status= status.HTTP_400_BAD_REQUEST) 
        
        
                
        #// here we need to check if discount was added 
        return_customer_discount = loyal_customer_discount
        q_price = quote_price 
        if(did_apply_loyal_discount == False):
            #// check if customer qualifies for discount 
            customer_bs = Booking.objects\
                                    .filter(booker = self.request.user)\
                                    .order_by('-created_at')
                                    
            if(len(customer_bs) >= 3):
                percentage = 10 #// percent %
                divider  = 100 #// percent 
                
                #// new price math.ceil(q*100)/100
                q_price = quote_price*((divider - percentage)/(divider))
                return_customer_discount = quote_price - q_price
                
        #// prices rounded to nearest two decimal 
        q_price_rounded = float("%.2f"%q_price)
        peak_discount_rounded = float("%.2f"%mid_month_discount)
        r_customer_discount_rounded = float("%.2f"%return_customer_discount)
                
        #// try and save the booking 
        try:
            #//now we need to save the booking 
            _booking = Booking.objects.create(
                        booker = loggedin_user,
                        pickup_date = pickup_date,
                        pickup_time = pickup_time,
                        payment_option = payment_option,
                        quote_price = q_price_rounded,
                        mid_month_discount =  peak_discount_rounded,
                        loyal_customer_discount = r_customer_discount_rounded,
                        distance_km = distance_km,
                        carry_floor = carry_floor,
                        vehicle_type = vehicle_type,
                        drivers_note = drivers_note,
                        additional_helpers = additional_helpers,
                        booking_completed = booking_completed,
                        booking_cancelled = booking_cancelled
                        ) 
            
        except Exception as e:
            payload['error_msg'] = str(e)
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        
        #// hard reset 
        try:
            #// otherwise everything is fine 
            for loc in routes:
                #// create locations instances 
                location  = LocationModel\
                                .objects\
                                .create(lat = loc['lat'], 
                                        lng = loc['lng'], 
                                        primary_text = loc['primary_text'],
                                        secondary_text = loc['secondary_text'],
                                        
                                        )
                #//loc_list.append(locaction)
                _booking.routes.add(location)

        except Exception as message:
            payload['error_msg'] = str(message)
            return Response(payload, status= status.HTTP_400_BAD_REQUEST)

        #_booking
        serializer = BookingSerializer(_booking , 
                                       many = False,  
                                       context = {'request': request},)
        #// return response 
        return Response(serializer.data, status = status.HTTP_201_CREATED)
        

class CustomerViewOwnBookingsListAPIView(generics.ListAPIView):
    
    queryset = Booking\
                .objects\
                .all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        
     
        #// customer bookings 
        customer_bs = None 
        
        #// perform mirabels 
        loggedin_user = request.user 

        #// here we need get a list of all the bookings 
        try:
            customer_bs = Booking.objects\
                                .filter(booker = loggedin_user)\
                                .order_by('-created_at')
        except Booking.DoesNotExist:
            # here we catch the error 
               #// 
            payload = dict()
            payload["response"] = str(status.HTTP_204_NO_CONTENT) + " Bad request"
            
            # we serialize the data 
            return Response(payload, status=status.HTTP_204_NO_CONTENT)
        
        
        #// here what we need to do 
        paginator = BookingsPaginator()
        results = paginator.paginate_queryset(customer_bs, request= request)
        serializer = BookingSerializer(results,
                                       many = True,
                                       context = {'request':request})
        
        return paginator.get_paginated_response(serializer.data)
 
 ## here we need to code a view that will return a view 
class CustomerGetBookingAPIView(generics.RetrieveAPIView):
    queryset = Booking\
                .objects\
                .all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated,]
 
# delete and update a booking 
class CustomerDeleteBookingDestroyAPIView(generics.DestroyAPIView):
    
    queryset = Booking\
                .objects\
                .all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated,]

    # delete booking 
    def delete(self, request, *args, **kwargs):
        
        # first thing 
        booking_pk = kwargs.get('pk') or None 
        if booking_pk is None:
            return Response(data={
                    "response": "null error",
                    "status_code": str(status.HTTP_400_BAD_REQUEST)
                },
                status=status.HTTP_400_BAD_REQUEST)
      
        obj_pk = get_object_or_404(Booking, pk = booking_pk)
        if obj_pk.booker == request.user:
            # check here if the current time is equal to the pickup_time 
            obj_pk.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        # return 
        return Response(status = status.HTTP_401_UNAUTHORIZED)
        #return self.destroy(request, *args, **kwargs)

# update api_view 
class UpdateBookingAPIView(generics.UpdateAPIView):
    
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'pk' # have to change and add slug field 
    
    # override put
    def put(self, request, *args, **kwargs):
    
        # ill get the pk 
        pk = kwargs.get('pk') or None 
        # check
        if pk is None:
            # send response 
            return Response(data={
                "response":"null response",
                "status":str(status.HTTP_400_BAD_REQUEST)
                }, 
                status=status.HTTP_400_BAD_REQUEST)

        # get the object
        booking = get_object_or_404(Booking, pk = pk)
        serializer = BookingSerializer(booking, data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class GenerateCustomerQuote(APIView):


    def _mid_month_discount(self, quotePrice, pickup_date):
        
        mid_month_discount = 0.0
        
        #// quote price threshold 
        threshold = 450 #// rands 
        
        #// this method must return a boolean 
        if(quotePrice <= threshold):
            return (quotePrice, mid_month_discount)
        
        #// other wise check the date 
        #// create getter for todays date 
        booking_date =  datetime.strptime(pickup_date, '%Y-%m-%d')
        
        #// check if date falls within the bounds for discount 
        min_day_threshold = 5 #// day
        max_day_threshold = 25 #// day 
        if(booking_date.day >= min_day_threshold and booking_date.day <= max_day_threshold):
            
            #// calculate the discount 
            discount = 10 #// percent 
            mid_month_discount = quotePrice*(discount/100.0)
            newQuotePrice = quotePrice - mid_month_discount
            
            #// return new quote price 
            return (newQuotePrice, mid_month_discount)
        
        #// here
        in_count = 15 #// percent 
        newQuotePrice = ((100 + in_count)/(100))*quotePrice
        
        # return 
        return (newQuotePrice, mid_month_discount)
    
    def generateLoyalCustomerDiscount(self, quotePrice):
        
        #// if customer is logged in 
        if(self.request.user.id != None):                      
            customer_bs = Booking.objects\
                                    .filter(booker = self.request.user)\
                                    .order_by('-created_at')
                                  
            if(customer_bs != None):
                # here we check when the last time the person created a booking with us 
                if(len(customer_bs) >= 3):
                    percentage = 10 #// percent %
                    divider  = 100 #// percent 
                    
                    #// new price 
                    quoteP = quotePrice*((divider - percentage)/(divider))
                    loyalC = quotePrice - quoteP
                    return (quoteP, loyalC, True)
                
        #other wise 
        return (quotePrice, 0.0, False)
  


    #// hadle 1.0 TONS CALCULATIONS
    def one_ton_stairs(self, carry_floors):
        
        #// check 
        if(carry_floors <= 0):return 0
        
        stairs = 0.0
        for index in range(carry_floors):
            stairs += (5*(index + 1) + 15)
        return stairs

    def one_ton(self, distance, carry_floors, additional_helpers):
        
        # set variables 
        base_amount = 430.0 #// rands (R)
        helper_fee = 90.0 #// rands (R)
        stairs_fee = self.one_ton_stairs(carry_floors) #// rands (R)
        price_per_km = 10.0 #// rands (R)
        tall_gate_fee = 0.0

        quotePrice = (
            (base_amount + tall_gate_fee) +  #// base + tall 
            (price_per_km*distance) +  #// petrol fee price_km x distance
            (stairs_fee) + #// stairs to carry 
            (helper_fee*additional_helpers)) #// helper fee
        
        return quotePrice


    #// hadle 1.0 TONS CALCULATIONS
    def onehalf_ton_stairs(self, carry_floors):
        
        if(carry_floors <= 0): return 0
        
        stairs = 0.0 
        for index in range(carry_floors):
            stairs += (5*(index + 1) + 25)
        return stairs

    def onehalf_ton(self, distance, carry_floors, additional_helpers):
        
        base_amount = 485.0 #// rands (R)
        helper_fee = 100.0 #// rands (R)
        stairs_fee = self.onehalf_ton_stairs(carry_floors) #// rands (R)
        price_per_km = 12.0 #// rands (R)
        tall_gate_fee = 0.0

        quotePrice = (
            (base_amount + tall_gate_fee) +  #// base + tall 
            (price_per_km*distance) +  #// petrol fee price_km x distance
            (stairs_fee) + #// stairs to carry 
            (helper_fee*additional_helpers)) #// helper fee
        
        return quotePrice

    #// handle 2.0 TONS CALCULATIONS
    def two_ton_stairs(self, carry_floors):
        
        if(carry_floors <= 0): return 0
        
        stairs = 0.0
        for index in range(carry_floors):
            stairs += (5*(index + 1) + 35)
        return stairs

    def two_ton(self, distance, carry_floors, additional_helpers):

        base_amount = 640.0 #// rands (R)
        helper_fee = 120.0 #// rands (R)
        stairs_fee = self.two_ton_stairs(carry_floors) #// rands (R)
        price_per_km = 14.0 #// rands (R)
        tall_gate_fee = 0.0

        quotePrice = (
            (base_amount + tall_gate_fee) +  #// base + tall 
            (price_per_km*distance) +  #// petrol fee price_km x distance
            (stairs_fee) + #// stairs to carry 
            (helper_fee*additional_helpers)) #// helper fee
        
        return quotePrice

    # generate quote 
    def _generateQuotePrice(self, distance, carry_floors, additional_helpers, vehicle_type):
        
        vehicle_one = 1.0 #// one ton
        vehicle_two = 1.5 #// 1.5 tons 
        vehicle_three = 2.0 #// 2.0 tons 
        
        if(float(vehicle_type) == vehicle_one):
            quotePrice = self.one_ton(distance, carry_floors, additional_helpers)
            return quotePrice
        elif(float(vehicle_type) == vehicle_two):
            quotePrice = self.onehalf_ton(distance, carry_floors, additional_helpers)
            return quotePrice
        elif(float(vehicle_type) == vehicle_three):
            quotePrice = self.two_ton(distance, carry_floors, additional_helpers)
            return quotePrice
        else:
            #// convert value to v_type  
            v_type = float(vehicle_type)
            if(v_type > vehicle_three):
                quotePrice = self.two_ton(distance, carry_floors, additional_helpers)
                return quotePrice*1.5
            else:
                quotePrice = self.two_ton(distance, carry_floors, additional_helpers)
                return quotePrice*1.5
        
    def post(self, request, *args, **kwargs):
        
        #// payload 
        payload = {}

        #// here we need to retrieve certain information from the front end
        distance = request.data.get('distance')  #// KiloMeters 
        vehicle_type = request.data.get('vehicle_type') 
        carry_floors = request.data.get('carry_floor')
        additional_helpers = request.data.get('additional_helpers')
        pickup_date = request.data.get('pickup_date')
        
        # here we talk to the customer 
        if(vehicle_type is None or carry_floors is None or additional_helpers is None or pickup_date is None):
            
            # create error message
            message = 'vehicle type, Floors to carry, additional Helpers or pickup date cannot be null. Bad request'
            
            # set the payload 
            payload['error_message'] = message
            payload['status_code'] = status.HTTP_400_BAD_REQUEST
            
            # response to the user 
            return Response(payload, status= status.HTTP_400_BAD_REQUEST)
        
        if(vehicle_type <= 0 or type(carry_floors) != int or type(additional_helpers) != int):
    
            # create error message
            message = 'vehicle type, Floors to carry or additional Helpers need to be an interger value'
            
            # set the payload 
            payload['error_message'] = message
            payload['status_code'] = status.HTTP_400_BAD_REQUEST
            
            # response to the user 
            return Response(payload, status= status.HTTP_400_BAD_REQUEST)
        
        # generate the quote self, distance, carry_floors, additional_helpers, vehicle_type
        generatedQuotePrice = self._generateQuotePrice(distance, 
                                                       carry_floors,
                                                       additional_helpers, 
                                                       vehicle_type)
        
        #// generate Off Peak discount/ Mid Month discount 
        quotePrice, middiscountPrice = self._mid_month_discount(generatedQuotePrice, pickup_date) #// rands 
        
        #// generate return customer discount 
        qp, loyaldiscount, did_apply_loyal_discount = self.generateLoyalCustomerDiscount(quotePrice)
        
        #// round values off to the nearest two decimal places 
        roundedQuotePrice = float("%.2f"%qp) # rounded to two decimal places 
        roundedLoyalDiscount = float("%.2f"%loyaldiscount) # rounded to two decimal places 
        roundedMiddiscountPrice = float("%.2f"%middiscountPrice) # rounded to two decimal places 
        
        #// calculate base quote price 
        baseQPrice = roundedQuotePrice + roundedLoyalDiscount + roundedMiddiscountPrice
        
        #// round off 
        roundedBaseQuotePrice = float("%.2f"%baseQPrice) # rounded to two decimal places 
        
        #// set payload 
        payload['message'] = 'Quote Successfully Generated'
        payload['generate_quote_price'] =  roundedQuotePrice
        payload['base_quote_price'] = roundedBaseQuotePrice
        payload['mid_month_discount'] =  roundedMiddiscountPrice
        payload['loyal_customer_discount'] =  roundedLoyalDiscount
        payload['did_apply_loyal_discount'] = did_apply_loyal_discount
        payload['status_code'] = status.HTTP_200_OK
        
        #// return payload 
        return Response(payload, status= status.HTTP_200_OK)

#// testing 
class GenerateDistanceBetweenTwoLocations(APIView):

    def post(self, request, *args, **kwargs):
        
        routes = request.data.get('routes') or None
        
        if(routes is None):
            return Response({'error_message': 'routes cannot be none'}, 
                            status = status.HTTP_400_BAD_REQUEST)

        try:
            for i in range(len(routes)-1):
                lat1 = float(routes[i]['lat'])
                lng1 = float(routes[i]['lng'])
                
                lat2 = float(routes[i+1]['lat'])
                lng2 = float(routes[i+1]['lng'])
                
                #// test 
                l1 = (lat1, lng1)
                g1 = (lat2, lng2)

                results = client.distance_matrix(l1, 
                                            g1,
                                            mode = 'driving')
                
                distance = float(results['rows'][0]['elements'][0]['distance']['value'])
                return Response({'distance': distance}, status=status.HTTP_200_OK)
        except Exception as e:
            
            message = 'Error {0}'.format(e)
            return Response({'error': message})
    
        