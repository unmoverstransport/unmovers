
from rest_framework.response import Response
from rest_framework import generics 
# Create your views here.

from faqs.models import FaqsModel
from faqs.serializers import FaqsSerializer

class FaqsRetrieveAPIView(generics.ListAPIView):
    queryset = FaqsModel\
                .objects\
                .all()
    serializer_class = FaqsSerializer
 

