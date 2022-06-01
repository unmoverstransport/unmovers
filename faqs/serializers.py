from rest_framework import serializers
from faqs.models import FaqsModel

class FaqsSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = FaqsModel
        fields = '__all__'
    
    