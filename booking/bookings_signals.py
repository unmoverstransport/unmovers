from django.db.models.signals import post_save
from django.dispatch import receiver
from booking.models import Booking

#email stuff 
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

#// send email 
@receiver(post_save, sender = Booking)
def send_invoice(sender, instance = None, created = False, **kwargs):
    
    if(created):
        
        #// customerfull name 
        full_name = str(instance.booker.first_name).capitalize() + ' ' + str(instance.booker.last_name).capitalize()
        
        #// round it off to remove all zeros
        base_fee = round(instance.quote_price + instance.mid_month_discount + instance.loyal_customer_discount, 2)
        
        #// this is what we want to pass 
        payload = dict()
        
        # //set payload
        payload["full_name"] = full_name
        payload["invoice_number"] = instance.id
        payload["base_fee"] = float("%.2f"%base_fee)
        payload["off_peak"] = instance.mid_month_discount
        payload["return_customer"] = instance.loyal_customer_discount
        payload["amount_due"] = instance.quote_price
        
        #set html
        html_content = render_to_string("booking_invoice.html", payload)
        text_content = strip_tags(html_content)
        
        #// send email 
        send_email = EmailMultiAlternatives(
            'UNITE NDLELA TRANSPORT SERVICES PTY(LTD) INVOICE {0}'.format(instance.id), #// subject 
            text_content, # content or body 
            settings.EMAIL_HOST_USER,
            ['u12318958@tuks.co.za', str(instance.booker.email), 'unitendlela@gmail.com'], #// receipiant list 
        )
        
        #// attach email html 
        send_email.attach_alternative(html_content, "text/html")
        
        #// silence any errors 
        send_email.fail_silently = True
        
        #// send email
        send_email.send()
        

