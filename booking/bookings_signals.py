from django.db.models.signals import post_save
from django.dispatch import receiver
from booking.models import Booking

#email stuff 
from django.core.mail import EmailMessage
from django.conf import settings

#// send email 
@receiver(post_save, sender = Booking)
def send_invoice(sender, invoice, **kwargs):
    
    invoice_instance_string = """

        Thank you very much for using our services
        below is your booking invoice
        
        INVOICE ID = {0}
        
        Booker = {1}
        Helpers = {2}
        distance(kilometers) = {3}
        Amount due = {4}
    
    """.format(
        invoice.id,
        invoice.booker,
        invoice.additional_helpers,
        invoice.distance_km,
        invoice.quote_price
    )
    
    #// send the mail 
    _email = EmailMessage(
        'UNITE NDLELA TRANSPORT SERVICES INVOICE', #// subject
        invoice_instance_string, #// message body 
        settings.EMAIL_HOST_USER, #// sender 
        ['u12318958@tuks.co.za'] #// receiver 
    )
    
    _email.fail_silently = True
    _email.send()

