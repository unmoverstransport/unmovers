#// import 
from rest_framework import generics 

#// import model 
from gallary.models import ItemGallaryModel

#// serializer 
from gallary.serializers import GallarySerializer


#// generic view 
class GallaryRetrieveAPIView(generics.ListAPIView):
    
    
    # these have to be set by default 
    queryset = ItemGallaryModel.objects\
                        .all()\
                        .order_by('-created_at')
    serializer_class = GallarySerializer
    
    

