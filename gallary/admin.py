from django.contrib import admin

# Register your models here.
from .models import ItemGallaryModel

# register model to site 
admin.site.register(ItemGallaryModel)