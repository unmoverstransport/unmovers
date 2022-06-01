# 3rd party local imports 
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ImageField
from rest_framework.authentication import get_user_model
# local imports 
from .models import NewUser, UserProfile

#// jwt imports 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# create seralizer 
class NewUserSerializer(ModelSerializer):
    #
    class Meta:
        model = NewUser
        fields = '__all__'
        
class UpdateUserSerializer(ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'mobile_number',]

class GetCompleteUserProfile(ModelSerializer):
    
    user = SerializerMethodField(read_only = True)
    image = SerializerMethodField('get_image', read_only = True)

    class Meta:
        model = UserProfile
        fields = [
                'user',
                'image',
                'created_at',
            ]
        
    def get_user(self, obj):
        if obj.user is None: return None
        _user = BookingNewUserSerializer(obj.user)
        return _user.data
    
    def get_image(self, obj):
        request = self.context.get('request')
        if request != None:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url
    

 # register serializer
class RegisterSerializer(ModelSerializer):
     
    class Meta:
         model = NewUser
         fields = ( 'email', 
                    'first_name', 
                    'last_name', 
                    'password', 
                    'is_customer', 
                    'is_driver', 
                    'is_staff',)
         extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class UserProfileSerializer(ModelSerializer):
    
    # otherwise this will be default userprofile serializer clas 
    class Meta:
        model = UserProfile
        fields = '__all__'
        

# CUSTOM USER BOOKING SERIALIZERS        
class BookingNewUserSerializer(ModelSerializer):
    # this will appear on the bookings 
    class Meta:
        model = NewUser
        fields = ['pk', 
                  'first_name', 
                  'last_name',
                  'mobile_number',
                  'is_customer',
                  'is_staff',
                  'is_driver']
        
class BookingUserProfileSerializer(ModelSerializer):
    
    # serializer method fields 
    user = SerializerMethodField(read_only = True)
    image = SerializerMethodField('get_image' ,read_only = True)

    # class meta 
    class Meta:
        model = UserProfile
        fields = ['image', 'user', 'created_at', ]
        
    # get the user details 
    def get_user(self, obj):
   
        # check 
        if obj.user is None: return None
        _user = BookingNewUserSerializer(obj.user)
        return _user.data
    
    def get_image(self, obj):
        request = self.context.get('request')
        if request != None:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url
    

    
    
#// custom JWT TOKEN SERIALIZER
class MoveItTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        #// we try and get the user profile 
        #// this might be an issue in the long run so we need to make 
        #// a plan and make sure that we find a better way of handling 
        #// this 
        userProfile = None 
        try:
            userProfile = UserProfile.objects.get(user = user)
        except UserProfile.DoesNotExist:
            userProfile = ''
            
        #// here we add 
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['image'] = userProfile.image.url
        
        #// return token 
        return token 
    
   
        
        