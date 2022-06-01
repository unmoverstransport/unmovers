from django.shortcuts import get_object_or_404
from rest_framework.authentication import get_user_model
from rest_framework import status
import json
from rest_framework.response import Response
from rest_framework import generics 
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.utils.translation import gettext_lazy as _

#// internal import 
from .serializer import ContactUseSerializer
from .models import ContactUs

class CreateContactMessageView(generics.CreateAPIView):
    
    serializer_class = ContactUseSerializer
    queryset = ContactUs.objects.all()
    permission_classes = [IsAuthenticated,]
    
    
    # here we create the message
    def post(self, request, *args, **kwargs):
        
        # // payload
        payload = dict()
        # // here we need to find the person who is currently logged in 
        currently_logged_in = request.user # this will always return a user 
        
        if currently_logged_in is not None:
            
            user = get_object_or_404(get_user_model(), pk = currently_logged_in.pk)
 
            payload["message"] = request.data["message"]
            payload["user"] = user.pk
       
            #// here we make sure that we serialize the data first before saving
            contact_use_serializer = ContactUseSerializer(data = payload)
            if contact_use_serializer.is_valid(raise_exception=True):
                contact_created = contact_use_serializer.save()
                if contact_created:
                    return Response({"status":"successfully created message"}, status=status.HTTP_201_CREATED)    
            return Response(contact_use_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        payload["status"] = 'You are unathorized to use this function'
        return Response(payload, status= status.HTTP_401_UNAUTHORIZED)       
    

    
    
   
    
    
    