from multiprocessing.sharedctypes import Value
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

# creat custom user baseusermanager 
class CustomAccountManager(BaseUserManager):
    
    user_in_migrations = True
    
    # here we do something
    def create_user(self, email, first_name, last_name, password, **other_fields):
        
        # check for email
        if not email:
            raise TypeError(_('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(email = email, first_name = first_name, 
                                        last_name = last_name, **other_fields)
        
        # set the password 
        user.set_password(password)
        user.save(using = self._db)
        
        return user 
    
    # create superuser 
    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_verified', True)
        
        # raise an exception 
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff = true')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser = true')
        if other_fields.get('is_active') is not True:
            raise ValueError('is_active must be assigned to is_active = true')
        if other_fields.get('is_verified') is not True:
            raise ValueError('is_verified must be set to is_verified = true')
        
        # create user 
        new_user = self.create_user(email, first_name, last_name, password, **other_fields)
        
        # return 
        return new_user
        
        