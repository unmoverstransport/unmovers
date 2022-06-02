

# third party package imports 
from email.policy import default
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from rest_framework_simplejwt.authentication import get_user_model
from rest_framework import serializers
# app imports 
from .managers import CustomAccountManager


# global functions 
def upload_to(instance, filename):
    return '/{filename}'.format(filename = filename)

def upload_id_copy_to(instance, filename):
    return '/{filename}'.format(filename = filename)

def upload_drivers_license_copy_to(instance, filename):
    return '/{filename}'.format(filename = filename)

# Create your models here.
class NewUser(AbstractBaseUser, PermissionsMixin):
    
    # define fields 
    email = models.EmailField(_('email address'), unique = True)
    first_name = models.CharField(max_length=150, null = True)
    last_name = models.CharField(max_length=150, null = True)
    mobile_number = models.CharField(max_length=50,
                                     null= True, blank= True)
    
    # dates 
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # unique identifies 
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    accepted_terms_and_conditions = models.BooleanField(default=True)
    
    # these are what determine the type of register
    is_staff = models.BooleanField(default=False) 
    is_customer = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    
    
    # setup user 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile_number']
    
    # override managers
    objects = CustomAccountManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}, pk = {self.pk}"
    
# create userprofile model
class UserProfile(models.Model):
    
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                null=True)
    image = models.ImageField(upload_to=upload_to, 
                                            default = 'profile_pics/default.jpg')
  
    # variables 
    id_number = models.PositiveBigIntegerField(null=True, blank=True)
    use_moveit_for = models.CharField(max_length=150,null = True, blank=True, default='private')
    
    # files 
    pdf_id_copy = models.FileField( 
                                   upload_to=upload_id_copy_to,
                                   null = True, blank=True)
    
    pdf_drivers_license_copy = models.FileField(
                                                upload_to=upload_drivers_license_copy_to,
                                                blank=True,
                                                null = True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.user.pk}"
    

            
            
    



