
# third party
from django.conf import settings as _set
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import UserProfile


# create signal  _set.AUTH_USER_MODEL
@receiver(post_save, sender = _set.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    
    # create token when user registers 
    if created:
        #Token.objects.create(user = instance)
        # we need to create user profile 
        try:
            UserProfile.objects.create(user = instance)
        except Exception as e:
            raise ValueError(e)

