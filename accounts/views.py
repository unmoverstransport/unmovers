
# third party imports 
import re
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from rest_framework import generics 
from rest_framework.authentication import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

from .models import UserProfile 
from .pagination import StaffDriverPaginator, CustomerPaginator
# local imports 
from .serializers import (GetCompleteUserProfile,
                        MoveItTokenObtainPairSerializer, 
                        RegisterSerializer, 
                        NewUserSerializer, 
                        UpdateUserSerializer, 
                        UserProfileSerializer)

# email stuff 
from django.core.mail import EmailMessage
from django.conf import settings

from random import randint
#// this is to retrieve user model for a specific user 
class GetUserAccountAPIView(APIView):
    
    permission_classes =  [IsAuthenticated,];
    
    def get(self, request, *args, **kwargs):
        
        # current User
        user = request.user
        user_model = get_object_or_404(get_user_model(), pk = user.pk)
        
        #// serialize data 
        user_model_serializer  = NewUserSerializer(user_model)
        return Response(user_model_serializer.data, status = status.HTTP_200_OK)


class AccountUserCreate(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        
        # create payload 
        payload = dict()
        # register serializer 
        reg_serializer = RegisterSerializer(data = request.data)
        if reg_serializer.is_valid(raise_exception=True):
            new_user = reg_serializer.save()
            if new_user:
                # set payload 
                payload['status'] = status.HTTP_201_CREATED
                payload['message'] = 'account successfully created'
                return Response(status=status.HTTP_201_CREATED)
            
            # set here
            payload['status'] = status.HTTP_400_BAD_REQUEST
            payload['message'] = 'was unable to create user for some reason'
            
            return Response(payload, status= status.HTTP_400_BAD_REQUEST)  
        return Response(reg_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class GetFullUserProfileView(APIView):
    
    permission_classes = [IsAuthenticated,]
    
    def get(self, request, *args, **kwargs):
        
        # lets get the registerd user 
        user = request.user
        user_obj = get_object_or_404(UserProfile, user = user)
        # serialize data 
        user_obj_serialized = GetCompleteUserProfile(user_obj);
        return Response(user_obj_serialized.data, status = status.HTTP_200_OK)
       
class AccountUserUpdateAPIView(APIView):
    
    permission_classes = [IsAuthenticated,]
    
    def put(self, request, *args, **kwargs):
        
        # function cannot detect wrong keys 
        user = request.user 
        payload = dict()
        if isinstance(user, get_user_model()):
            user_model = get_object_or_404(get_user_model(), pk = user.pk)
            user_serializer = UpdateUserSerializer(user_model, data=request.data)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        payload["error"] = "not authenticated"
        return Response(payload, status=status.HTTP_401_UNAUTHORIZED)


class AccountProfileUpdateAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        
        # get user profile 
        user_profile = get_object_or_404(UserProfile, user = request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
# logout 
class BlackListTokenView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            user = request.user 
            tokens = OutstandingToken.objects.filter(user_id = user.id)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token = token)
            # refresh_token = request.data.get('refresh_token')
            # token = RefreshToken(refresh_token)
            # token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status = status.HTTP_400_BAD_REQUEST)

# delete user 
class DeleteUserAPIView(APIView):
    
    permission_classes = [IsAuthenticated,]
   
    def delete(self, request, *args, **kwargs):
        
        # check if user is authenticated
        if request.user.is_authenticated:
            instance = get_object_or_404(get_user_model(), pk = request.user.pk)
            instance.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)

# staff view 
class DriverUpdateAPIView(generics.UpdateAPIView):
    
    queryset = get_user_model()\
                .objects.all()\
                .order_by('-date_joined')
            
    serializer_class = UpdateUserSerializer
    permission_class = [IsAuthenticated,] #Custom authentication for staff
    
    lookup_field = 'pk'
    
    def put(self, request, *args, **kwargs):
      
        pk = kwargs.get('pk') or None 
        if pk is None: return Response(status=400)
        
        # lets get the user 
        user = get_object_or_404(get_user_model(), pk = pk)
        if user.is_driver:
            user_serializer = UpdateUserSerializer(user, data=request.data)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                return Response(user_serializer.data,status = status.HTTP_200_OK)
            return Response(user_serializer.error, status = status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"user not driver"}, status = status.HTTP_400_BAD_REQUEST)

        
class DriverDeleteAPIView(generics.DestroyAPIView):
    queryset = get_user_model()\
                .objects\
                .all()
    serializer_class = NewUserSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated,]
    
    def delete(self, request, *args, **kwargs):
        
        # check if pk exists and set payload to default
        payload = dict()
        driver_pk = kwargs.get('pk') or None 
        if driver_pk is None:
            return Response({"msg":"pk cant be none"}, status= 400)
        
        # other wise 
        driver = get_object_or_404(get_user_model(), pk = driver_pk)
        if driver.is_driver:
            driver.delete()
            payload["msg"] = "successfully deleted"
            return Response(payload, status = status.HTTP_204_NO_CONTENT)
        payload["msg"] = "user is not a driver"
        return Response(payload, status=400)

class DriverListAPIView(generics.ListAPIView):
    
    queryset = get_user_model()\
                .objects\
                .filter( is_driver = True)\
                .order_by('-date_joined')
                
    serializer_class = NewUserSerializer
    pagination_class = StaffDriverPaginator
    
    # custom permissions for the admin and super user 
    
class CustomerListAPIView(generics.ListAPIView):
    
    queryset = get_user_model()\
                .objects\
                .filter( is_customer = True)\
                .order_by('-date_joined')
                
    serializer_class = NewUserSerializer
    pagination_class = CustomerPaginator
    
    # custom permissions for the admin and super user 

#// we need to personalize the token 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MoveItTokenObtainPairSerializer


#// this is new please enter it in the server 
class RecoverAccountAPIView(APIView):

    def post(self, request, *args, **kwargs):
        
        # set payload 
        payload = dict()
        
        #// here we need to get the email address 
        recovery_email = request.data.get('recovery_email') or None 
        
        if(recovery_email is None):
            
            # set payload 
            payload['error_msg'] = 'recovery email cannot be none'
            payload['status_code'] = status.HTTP_400_BAD_REQUEST
            
            # //return 
            return Response(payload, status = status.HTTP_400_BAD_REQUEST)
        
        #other wise everything is dope 
        #get user with similar email 
        user = get_user_model()\
                    .objects\
                    .filter(email = recovery_email)\
                    .first() or None 
                    
        #// check
        if(user is None):
            
            # set payload 
            payload["msg"] = "user with the current email doesnt exist "
            payload["status"] = status.HTTP_404_NOT_FOUND
            
            #// return 
            return Response(payload, status.HTTP_404_NOT_FOUND) 
        
        # here we generate the unique 6 digit pin 
        six_digit_pin = randint(100000, 999999)
        
        # here we send the email to the user 
        reset_password_email_body = """
        Hi {0}, Thank you very much for Using Our Services. 
        
        Here's your unique six digit pin to reset your password 
        
        PIN CODE: {1}
        
        if you have any questions please kindly send us an email to this email 
        address: unitendlela@gmail.com and one of our consultants will response
        to you as soon as possible. 
        
        Kind Regards 
        Unite Ndlela Transport Services Admin
        email: unitendlela@gmail.com
        phone No: 0844394032
        """.format(
            str(user.first_name) + " " + str(user.last_name),
            six_digit_pin,
        )
        
        # email sender 
        email_sender = EmailMessage(
            'UNITE NDLELA TRANSPORT SERVICES PTY(LTD)',
            reset_password_email_body,
            settings.EMAIL_HOST_USER,
            ['u12318958@tuks.co.za', str(user.email)] 
        )
           
        email_sender.fail_silently = True
        email_sender.send()

        #// we will have to generate a unique 6 digit pin to send to their email to reset password 
        payload["msg"] = "Success!, an email with a 6 digit pin was sent to {0}".format(recovery_email)
        payload["status"] = status.HTTP_200_OK
        payload["six_digit_pin"] = six_digit_pin
        
        return Response(payload, status = status.HTTP_200_OK)

