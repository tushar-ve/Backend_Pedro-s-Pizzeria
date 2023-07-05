from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from .renderers import *
from rest_framework_simplejwt.tokens import RefreshToken
from .email import *
from rest_framework.permissions import IsAuthenticated
# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_otp_via_email(serializer.data['email'])
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Verify OTP

class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer= VerifyAccountSerializer(data=data)
             
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = User.objects.filter(email= email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message' : 'something went wrong',
                        'data': 'invalid email'
                    })
                
                if user.otp != otp:
                    return Response({
                        'status': 400,
                        'message' : 'something went wrong',
                        'data': 'invalid OTP'
                    })
                user = user.first()
                user.is_verified = True
                user.save()

                return Response({
                        'status': 200,
                        'message' : 'Accoumt verified',
                        'data': {}
                    })
        except:
            return Response({
                        'status': 400,
                        'message' : 'something went wrong',
                        'data': 'invalid OTP'
                    })


# acessing menu 
class MenuDescriptionView(APIView):
    # renderer_classes = [UserRenderer]

    def get(self, request, item_id):
        try: 

            menu_item_obj = MenuItem.objects.get(id=item_id)
            print(item_id)
            serializer = MenuItemSerializer(menu_item_obj) 
            print(request.data)        
            return Response(serializer.data, status=status.HTTP_200_OK)

        except MenuItem.DoesNotExist:
            return Response({'status': 404, 'message': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'status': 403, 'message': 'Menu item doesnot exists'}, status=status.HTTP_403_FORBIDDEN)



class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token,'msg':'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors' : {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
        renderer_classes = [UserRenderer]
        permission_classes= [IsAuthenticated]
        def get(self, request, format=None):
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        


class UserChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data= request.data, context={'user':request.user})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password has been changed'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SendPasswordResetEmailView(APIView):
    
    renderer_classes=[UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data= request.data)

        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Link has been sent, Please Check your Inbox'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
    

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
  

class MenuView(APIView):
    renderer_classes=[UserRenderer]
    def get(self, request):
        Menu_objs = MenuItem.objects.all()
        serializer = MenuItemSerializer(Menu_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class AboutUsView(APIView):
    renderer_classes = [UserRenderer]
    def get(self, request):
        About_objs = AboutUsModel.objects.all()
        serializer = AboutUsSerializer(About_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


