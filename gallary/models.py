#// imports 
from django.db import models
from django.utils.translation import gettext_lazy as _



#// upload function 
def upload_to_gallary(instance, filename):
    return '{filename}'.format(filename = filename)

#// gallary model
class ItemGallaryModel(models.Model):
    
    image_gallary = models.ImageField(upload_to=upload_to_gallary)
    # created at 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    