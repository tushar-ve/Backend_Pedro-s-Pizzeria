from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.utils.text import slugify

#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, tc, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          tc=tc,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, tc, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          tc=tc,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  tc = models.BooleanField()
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_verified = models.BooleanField(default= False, blank=False)
  otp = models.CharField(max_length=6, null=True, blank=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'tc']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin


class MenuItem(models.Model):
    name= models.CharField(max_length=255)
    image= models.ImageField(upload_to='Images/')
    detail = models.CharField(max_length=2000)
    ingredients = models.CharField(max_length=500)
    veg= models.BooleanField(default=True)
    amount= models.BigIntegerField()
    energy = models.IntegerField()
    carbs= models.IntegerField()
    protein = models.IntegerField()
    fibre = models.IntegerField()
    fat = models.IntegerField()
    rating= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numreviews = models.IntegerField(null=True, blank=True, default=0)
    createdAt= models.DateTimeField(auto_now=True)
    countInStock= models.IntegerField(null=True, blank=True, default=0)

    


    def __str__(self):
        return self.name

class AboutUsModel(models.Model):
    description = models.TextField(max_length=1000)
    des_title= models.CharField(max_length=300)

    def __str__(self) :
        return self.des_title
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.email} - {self.item.name}"


class Order(models.Model):

    SIZES=(
        ('SMALL','small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
    )

    ORDER_STATUS=(
        ('PENDING', 'pending'),
        ('IN_TRANSIT','inTransit'),
        ('DELIVERED','delivered'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    size= models.CharField(max_length=25, choices=SIZES, default=SIZES[0][0])
    order_status= models.CharField(max_length=20, choices=ORDER_STATUS, default=ORDER_STATUS[0][0])
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.email} - {self.item.name}"


