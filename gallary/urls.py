from django.urls import path


# local imports 
from . import views


# check 
urlpatterns = [
    
    # one more thing to do, include in our serializers 
    
    # complete set of urls
    path('', views.GallaryRetrieveAPIView.as_view(), 
                    name = 'gallary-view'), # this is to be viewed by staff

    
]