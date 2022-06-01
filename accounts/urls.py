from django.urls import path
#from rest_framework.authtoken.views import obtain_auth_token

# local imports 
from . import views 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# check 
urlpatterns = [
    
    # register/delete_user/login/refresh_token/logout/update userprofile
    path('api/register/', views.AccountUserCreate.as_view(), name = 'register-view'),
    path('api/delete-user/', views.DeleteUserAPIView.as_view(), name='delete-user'),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'), # this is to login 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # this is to refresh the token
    path('api/token/blacklist/', views.BlackListTokenView.as_view(), name='blacklist-view'), # this is to logout
    path('api/update/userprofile/', views.AccountProfileUpdateAPIView.as_view(), name= 'update-profile'),
    path('api/update/user/', views.AccountUserUpdateAPIView.as_view(), name = 'update-user'),
    path('api/get/user/', views.GetFullUserProfileView.as_view(), name = 'get-userprofile'),
    # these are for the stuff 
    path('api/drivers/', views.DriverListAPIView.as_view(), name = 'drivers-view'),
    path("api/driver/<int:pk>/update/", views.DriverUpdateAPIView.as_view(), name="update-driver"),
    path("api/driver/<int:pk>/delete/", views.DriverDeleteAPIView.as_view(), name="delete-driver"),
     path('api/customers/', views.CustomerListAPIView.as_view(), name = 'customers-view'),
]