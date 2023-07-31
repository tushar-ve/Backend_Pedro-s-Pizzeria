from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
# Register your models here.


class UserModelAdmin(BaseUserAdmin):
    # The forms to add and change user instances
  

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "name","tc", "is_admin", "is_verified"]
    list_filter = ["is_admin"]
    fieldsets = [
        ('User Credentials', {"fields": ["email", "password", "is_verified"]}),
        ("Personal info", {"fields": ["name", "tc"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name","tc", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = []

admin.site.register(User, UserModelAdmin)

admin.site.register(MenuItem)

admin.site.register(AboutUsModel)
admin.site.register(Address_Order)


class CartItemAdmin(admin.ModelAdmin):
    list_display=['id','item', 'quantity']

admin.site.register(CartItem)


class OrderAdmin(admin.ModelAdmin):
    list_display=['id','customer','order_status','size','created_at']
    list_filter=['updated_at','order_status']

admin.site.register(Order, OrderAdmin)


admin.site.register(Payment)