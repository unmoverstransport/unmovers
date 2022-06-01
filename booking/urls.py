from django.urls import path


# local imports 
from . import views


# check 
urlpatterns = [

    # complete set of urls
    path('', views.CustomerBookingsListAPIView.as_view(), 
                    name = 'bookings-view'), # this is to be viewed by staff

    path('customer/list/', 
            views.CustomerViewOwnBookingsListAPIView.as_view(),
                name  = 'customer-bookings-list'),
    
    path('customer/create/', 
            views.CustomerViewOwnBookingsCreateAPIView.as_view(),
                name  = 'customer-booking-create'),
    
    path('delete-booking/<str:pk>/', views.CustomerDeleteBookingDestroyAPIView.as_view(),
                name='delete-booking'),
    
    path('update-booking/<str:pk>/', views.UpdateBookingAPIView.as_view(), name = 'update-booking'),
    
    path('retrieve-booking/<str:pk>/', views.CustomerGetBookingAPIView.as_view(), name = 'retrieve-booking'),
    
    # generate quote price 
    path('generate-quote-price/', views.GenerateCustomerQuote.as_view(), name = 'generate-quote-price'),
    
    
    #// testing url 
    path('distance-calculator/', views.GenerateDistanceBetweenTwoLocations.as_view(), name = 'distance-calculator')
    
    
]