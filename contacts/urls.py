from django.urls import path


# local imports 
from . import views


# check 
urlpatterns = [
    
    # one more thing to do, include in our serializers 
    path('', views.CreateContactMessageView.as_view(), name = 'contact-us'),
    
]