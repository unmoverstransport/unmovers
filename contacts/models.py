from django.db import models
from rest_framework.authentication import get_user_model
from django.utils.translation import gettext_lazy as _


# Create your models here.
class ContactUs(models.Model):
    
    user = models.ForeignKey(get_user_model(), 
                             on_delete=models.SET_NULL,
                                related_name=_('contact_user'), 
                                    null=True)
    
    message = models.TextField(max_length = 1000, default = '')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    # done 
    def __str__(self):
        return f'{self.user}'