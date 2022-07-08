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
        
        
        html_content = render_to_string("booking_invoice.html")
        text_content = strip_tags(html_content)
        
        #// send email 
        send_email = EmailMultiAlternatives(
            'UNITE NDLELA TRANSPORT SERVICES', #// subject 
            
            text_content, # content or body 
            settings.EMAIL_HOST_USER,
            ['u12318958@tuks.co.za'], #// receipiant list 
        )
        send_email.attach_alternative(html_content, "text/html")
        send_email.fail_silently = True
        send_email.send()
        
        # invoice_instance_string = """
            
        #     Hi {0} {1}
        #     UNITE NDLELA TRANSPORT SERVICES would like to Thank you for using our services
        #     below is your booking Slip
            
        #     SLIP:
        #     Requested Helpers = {2}
        #     Stairs to Carry = {3}
        #     distance(kilometers) = {4}(kms)
        #     Amount due = R {5}
        #     Booking Date = {6}
        #     Booking Time = {7}
            
        #     One of our drivers will be asigned to your booking and will contact you
        #     via email or phone number once they're on their way to attend to your booking
            
        #     if you have any questions, please kindly send us an email to this email 
        #     address: unitendlela@gmail.co, one of our consultants we'll response to you as 
        #     soon as possible. 
            
        #     Kind Regards 
        #     Unite Ndlela Transport Services Admin
        #     email: unitendlela@gmail.com
        #     phone No: 0844394032
        # """.format(
        #     str(instance.booker.first_name) + ' ' + str(instance.booker.last_name), #// 0
        #     '{0}'.format(instance.booker.email), #//1
        #     instance.additional_helpers, #//2
        #     instance.carry_floor, #// 3
        #     instance.distance_km, #// 4
        #     instance.quote_price, #// 5
        #     instance.pickup_date, #// 6
        #     instance.pickup_time, #// 7
        # )
        
        # #// send the mail 
        # email_sender = EmailMessage(
        #     'UNITE NDLELA TRANSPORT SERVICES PTY(LTD) INVOICE {0}'.format(instance.id), #// subject
        #     invoice_instance_string, #// message body 
        #     settings.EMAIL_HOST_USER, #// sender 
        #     ['u12318958@tuks.co.za', 
        #      '{0}'.format(instance.booker.email), 
        #      'unitendlela@gmail.com'] #// receiver 
        # )
        
        # email_sender.fail_silently = True
        # email_sender.send()

