from re import search
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# local imports 
from .models import NewUser, UserProfile


# customize the admin panel
class UserAdminConfig(UserAdmin):
    
    search_fields = ('email',
                     'first_name')
    
    list_filter = ('email',
                   'first_name',
                   'last_name',
                   'is_active')
    ordering = ('-date_joined', )
    
    list_display = ('email',
                    'first_name', 
                    'last_name', 
                    'is_active', 
                    'is_staff',
                    'date_joined')
    
    fieldsets = (
        (None, {'fields': ('email',
                           'first_name', 
                           'last_name',
                           'mobile_number',
                           'password',)}),
        
        ('Permissions', {'fields': ('is_staff',
                                    'is_active',
                                    'is_verified',
                                    'is_superuser',
                                    'is_customer',
                                    'is_driver',)}),
        
#('Personal', {'fields': ('pdf_id_copy',
#                                 'pdf_drivers_license_copy',)})
    )
    
    # check new
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'first_name',
                       'last_name','password1',
                       'password2',
                        'is_active',
                        'is_staff',
                        'is_verified'),
        }),
    )


# register to the site 
admin.site.register(NewUser, UserAdminConfig)
admin.site.register(UserProfile)
