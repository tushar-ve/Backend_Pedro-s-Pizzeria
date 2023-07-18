from rest_framework import serializers
from xml.dom import ValidationErr
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields= ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs={
            'password':{'write_only':True}
        }

        # validating password & confirm password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password & confirm  Password doesn't match")
            
        return attrs
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password', 'is_verified']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs
  



class SendPasswordResetEmailSerializer(serializers.Serializer):
   email = serializers.EmailField(max_length=255)
   class Meta:
      fields=['email']

   def validate(self, attrs):
      email = attrs.get('email')
      if User.objects.filter(email=email).exists():
         user = User.objects.get(email = email)
         uid = urlsafe_base64_encode(force_bytes(user.id))
         print('Enoded UID', uid)
         token = PasswordResetTokenGenerator().make_token(user)
         print('Password Reset Token', token)

         link = 'http://localhost:3000/reset-password/'+uid+'/'+token

         print('Password Reset Link', link)
         body = 'Click Following Link to Reset Your Password '+link
         data = {
              'subject':'Reset Your Password',
              'body':body,
              'to_email':user.email
            }
         Util.send_email(data)
         
         return attrs

      else:
         raise ValidationErr('This mail is not register')
      

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
    


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

# class MenuItemSearchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MenuItem
#         fields = ['name']


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsModel
        fields = '__all__'



class VerifyAccountSerializer(serializers.Serializer):
   email = serializers.EmailField()
   otp = serializers.CharField()
   class Meta:
      model= User
      fields=['otp', 'email']


class CartItemSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(

        queryset=MenuItem.objects.all(), write_only=True)




    amount = serializers.DecimalField(

        source='item.amount', max_digits=10, decimal_places=2, read_only=True)

    image = serializers.ImageField(source='item.image', read_only=True)

    name = serializers.CharField(source='item.name', read_only=True)
    class Meta:

        model = CartItem

        fields = ['id', 'user', 'item',

                  'quantity', 'name', 'amount', 'image']



class OrderSerializer(serializers.ModelSerializer):
    order_status=serializers.HiddenField(default="PENDING")
    size=serializers.CharField(max_length=25)
    quantity=serializers.IntegerField()
    

    class Meta:
        model=Order 
        fields=['order_status', 'size', 'quantity','item']


class OrderDetailSerializer(serializers.ModelSerializer):
   order_status=serializers.CharField()
   size=serializers.CharField(max_length=25)
   quantity=serializers.IntegerField()
   created_at= serializers.DateTimeField()
   updated_at= serializers.DateTimeField()

   class Meta:
        model=Order 
        fields=['order_status', 'size', 'quantity','item','created_at','updated_at']


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
   order_status=serializers.CharField()

   class Meta:
      model=Order 
      fields=['order_status']