#// imports 
from django.db import models
from django.utils.translation import gettext_lazy as _
import dropbox

dxv = dropbox.Dropbox('sl.BIwoH7kttAAtVu0Qxbx8AUoImi34-duNu9ALsTKS_Y5_UIxISJ1hu5lCoiUQI7Jho-8d2RtXOBXLgfm4Xu5TIRQOpGjAcRrQD1UO67Dy3pmEYv3CMQ2SxwD0nRSh6pz_rd85Czh7Tec')


#// upload function 
def upload_to_gallary(instance, filename):
    return 'gallary/{filename}'.format(filename = filename)

#// gallary model
class ItemGallaryModel(models.Model):
    
    image_gallary = models.ImageField(_("image_gallary"), upload_to=dxv.files_upload)
    # created at 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    