from django.contrib import admin

# Register your models here.
from .models import ContactUs


# register model to site 
admin.site.register(ContactUs)