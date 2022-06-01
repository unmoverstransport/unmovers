from rest_framework.serializers import ModelSerializer, SerializerMethodField, ImageField
from gallary.models import ItemGallaryModel

class GallarySerializer(ModelSerializer):
    
    class Meta:
        
        model = ItemGallaryModel
        fields = '__all__'
    
    