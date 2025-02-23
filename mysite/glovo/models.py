from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(65)], null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_image/')
    phone_number = PhoneNumberField(null=True, blank=True)
    STATUS_CHOICES = (
        ('client', 'client'),
        ('owner', 'owner'),
        ('courier', 'courier')
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=16, default='client')
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=32)

    def __str__(self):
        return self.category_name

class Store(models.Model):
    store_name = models.CharField(max_length=32)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_store')
    description = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    store_image = models.ImageField(upload_to='store_images/')

    def __str__(self):
        return self.store_name


    def get_count_people(self):
       ratings = self.store_review.all()
       if ratings.exists():
           total = ratings.count()
           if total > 2:
               return '2+'
           return total
       return 0


    def get_good_stars(self):
        ratings = self.store_review.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.stars > 3:
                    total+=1
            return f'{round((total * 100) / ratings.count())}%'

        return f'0%'


class Contact(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='contact')
    title = models.CharField(max_length=32)
    contact_number = PhoneNumberField()
    social_network = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}, {self.contact_number}'


class Product(models.Model):
    product_name = models.CharField(max_length=64)
    description = models.TextField()
    product_image = models.ImageField(upload_to='product_image/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_list')

    def __str__(self):
        return f'{self.product_name}'


class Combo(models.Model):
    combo_name = models.CharField(max_length=64)
    description = models.TextField()
    combo_image = models.ImageField(upload_to='combo_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='combo_list')

    def __str__(self):
        return self.combo_name

class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)


class Order(models.Model):
    client_order = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="client_orders")
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=32)
    ORDER_STATUS_CHOICES = (
        ('ожидает обработки', 'ожидает обработки'),
        ('доставлен', 'доставлен'),
        ('в процессе доставки', 'в процессе доставки'),
        ('отменен', 'отменен')
    )
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=64, default='доступен')
    courier_order = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="courier_orders")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_order}, {self.courier_order}'


class Courier(models.Model):
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    current_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    COURIER_STATUS_CHOICES = (
        ('доступен', 'доступен'),
        ('занят', 'занят')
    )
    courier_status = models.CharField(choices=COURIER_STATUS_CHOICES, max_length=16, default='доступен')

    def __str__(self):
        return f'{self.courier}, {self.courier_status}'



class StoreReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_review')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_review')
    stars = models.IntegerField(choices=[(i, str(i)) for i in range (1, 11)])
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.store}'


class CourierReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='clients')
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='couriers')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1,6)])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.courier}'