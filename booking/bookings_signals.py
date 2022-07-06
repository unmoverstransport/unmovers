from django.db.models.signals import post_save
from django.dispatch import receiver
from booking.models import Booking

#email stuff 
from django.core.mail import EmailMessage
from django.conf import settings

#// send email 
@receiver(post_save, sender = Booking)
def send_invoice(sender, instance = None, created = False, **kwargs):
    
    if(created):
        invoice_instance_string = """
            
            Hi {1} {2}
            UNITE NDLELA TRANSPORT SERVICES would like to Thank you for using our services
            below is your booking Slip
            
            SLIP:
            Requested Helpers = {3}
            Stairs to Carry = {4}
            distance(kilometers) = {5}(kms)
            Amount due = R {6}
            
            One of our drivers will be asigned to your booking and will contact you
            via email or phone number once they're on their way to attend to your booking
            
            if you have any questions, please kindly send us an email to this email 
            address: unitendlela@gmail.co, one of our consultants we'll response to you as 
            soon as possible. 
            
            Kind Regards 
            Unite Ndlela Transport Services Admin
            email: unitendlela@gmail.com
            phone No: 0844394032
        """.format(
            str(instance.booker.first_name) + ' ' + str(instance.booker.last_name),
            '{0}'.format(instance.booker.email),
            instance.additional_helpers,
            instance.carry_floor,
            instance.distance_km,
            instance.quote_price
        )
        
        #// send the mail 
        email_sender = EmailMessage(
            'UNITE NDLELA TRANSPORT SERVICES PTY(LTD) INVOICE {0}'.format(instance.id), #// subject
            invoice_instance_string, #// message body 
            settings.EMAIL_HOST_USER, #// sender 
            ['u12318958@tuks.co.za', 
             '{0}'.format(instance.booker.email), 
             'unitendlela@gmail.com'] #// receiver 
        )
        
        email_sender.fail_silently = True
        email_sender.send()

