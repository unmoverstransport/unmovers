
# third party
from django.conf import settings as _set
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import UserProfile


#email stuff 
from django.core.mail import EmailMessage
from django.conf import settings


# create signal  _set.AUTH_USER_MODEL
@receiver(post_save, sender = _set.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    
    # create token when user registers 
    if created:
        #Token.objects.create(user = instance)
        # we need to create user profile 
        try:
            UserProfile.objects.create(user = instance)
            
            #// here we need to create an email
            #// successfully registerd with us body message 
            register_message = """
            UNITE NDLELA TRANSPORT SERVICES
            
            
            Hi {0} {1}, Thank you very much for registering with 
            Unite Ndlela Transport services. 
            
            if you have any questions please kindly send us an email to this email 
            address: unitendlela@gmail.com and one of our consultants will response
            to you as soon as possible. 
            
            Kind Regards 
            Unite Ndlela Transport Services Admin
            email: unitendlela@gmail.com
            phone No: 0844394032
            """.format(instance.first_name, instance.last_name)
                  
            #// send the mail 
            email_sender = EmailMessage(
                'UNITE NDLELA TRANSPORT SERVICES PTY(LTD)', #// subject
                register_message, #// message body 
                settings.EMAIL_HOST_USER, #// sender 
                ['u12318958@tuks.co.za', str(instance.email)] #// receiver 
            )
            
            email_sender.fail_silently = True
            email_sender.send()
        except Exception as e:
            raise ValueError(e)

