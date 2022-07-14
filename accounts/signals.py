
# third party
from django.conf import settings as _set
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import UserProfile


#email stuff 
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

#safe 
from decouple import config


# create signal  _set.AUTH_USER_MODEL
@receiver(post_save, sender = _set.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    
    # create token when user registers 
    if created:
        #Token.objects.create(user = instance)
        # we need to create user profile 
        try:
            UserProfile.objects.create(user = instance)
            
            #// set values 
            full_name = str(instance.first_name).capitalize() + ' ' + str(instance.last_name).capitalize()
            
            #// payload 
            payload = dict()
            
            #// set payload 
            payload['full_name'] = full_name
            
            #// set html
            html_content = render_to_string("new_customer.html", payload)
            text_content = strip_tags(html_content)
            
            #// send email 
            send_email = EmailMultiAlternatives(
                'UNITE NDLELA TRANSPORT SERVICES PTY(LTD)', #// subject 
                text_content, # content or body 
                settings.EMAIL_HOST_USER,
                [config('PERSONAL_EMAIL', cast=str), str(instance.email)], #// receipiant list 
            )
            
            #// attach email html 
            send_email.attach_alternative(html_content, "text/html")
            
            #// silence any errors 
            send_email.fail_silently = True
            
            #// send email
            send_email.send()
            
        except Exception as e:
            raise ValueError(e)

