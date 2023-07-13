"""
URL configuration for api_food project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('change-password/', UserChangePasswordView.as_view()),
    path('emailreset-password/', SendPasswordResetEmailView.as_view()),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view()),
    path('menuitems/', MenuView.as_view()),
    path('aboutus/', AboutUsView.as_view()),
    path('verify/', VerifyOTP.as_view()),
    path('get-names/',SearchMenuAPIView.as_view()),
    path('menuitems/<str:item_id>/', MenuDescriptionView.as_view()),
    path('add-cart/', CartItemListCreateAPIView.as_view()),
    path('order/', OrderCreateView.as_view()),
    path('order/<str:order_id>',OrderDetailView.as_view()),
    path('update-status/<str:order_id>/', UpdateOrderStatus.as_view()),
    path('user/<str:user_id>/orders/', UserOrderView.as_view()),
    path('user/<str:user_id>/orders/<str:order_id>/', UserOrderDetail.as_view())
]
