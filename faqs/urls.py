from django.urls import path


# local imports 
from . import views


# check 
urlpatterns = [
    
    # one more thing to do, include in our serializers 
    
    # # complete set of urls
    path('', views.FaqsRetrieveAPIView.as_view(), 
                    name = 'faqs-view'), # this is to be viewed by staff

    
]