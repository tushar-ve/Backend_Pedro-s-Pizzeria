from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from .renderers import *
from rest_framework_simplejwt.tokens import RefreshToken
from .email import *
from django.shortcuts import get_object_or_404

# from rest_framework.filters import SearchFilter
from django.http import JsonResponse
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
                
                if otp != otp:
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
                        'message' : 'Account verified',
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

# search on the basis of Name
class SearchMenuAPIView(APIView):
    def get(self, request):
        search = request.GET.get('name')
        if search:
            items = MenuItem.objects.filter(name__icontains=search)
            serializer = MenuItemSerializer(items, many=True)
            print(items)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 404, 'message': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            is_verified= serializer.data.get('is_verified')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token,'is_verified':is_verified,'msg':'Login Success'}, status=status.HTTP_200_OK)
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




class CartItemListCreateAPIView(APIView):
    def get(self, request):
        cart_items = CartItem.objects.get(user=request.id)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderCreateView(APIView):
    permission_classes=[IsAuthenticated]
    # serializer_class=serializers.OrderSerializer

    def get(self,request):
        orders=Order.objects.all()

        serializer= OrderSerializer(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
            

    def post(self, request):
            data=request.data

            serializer= OrderSerializer(data=data)
            
            user= request.user


            if serializer.is_valid(raise_exception=True):
                serializer.save(customer=user)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(data==serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderDetailView(APIView):
    
    permission_classes=[IsAuthenticated]

    def get(self,request,order_id):
         
        try: 

            menu_item_obj = Order.objects.get(id=order_id)
            print(order_id)
            serializer = OrderDetailSerializer(menu_item_obj) 
            print(request.data)        
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,order_id):
        data=request.data
        menu_item_obj = Order.objects.get(id=order_id)

        serializer = OrderDetailSerializer(menu_item_obj, data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,order_id):
        menu_item_obj = Order.objects.get(id=order_id)

        menu_item_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UpdateOrderStatus(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request, order_id):
        menu_item_obj = Order.objects.get(id=order_id)

        data= request.data

        serializer = OrderStatusUpdateSerializer(menu_item_obj, data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrderView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request, user_id):
        try:
            user=User.objects.get(pk=user_id)
            
            orders= Order.objects.all().filter(customer=user)
            serializer = OrderDetailSerializer(orders, many=True)

            return Response(data= serializer.data, status=status.HTTP_200_OK)
        except:
         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserOrderDetail(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,user_id,order_id):
        try:
            user=User.objects.get(pk=user_id)

            order= Order.objects.all().filter(customer=user).filter(pk=order_id)
            serializer = OrderDetailSerializer(order, many=True)

            return Response(data= serializer.data, status=status.HTTP_200_OK)

        except:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


