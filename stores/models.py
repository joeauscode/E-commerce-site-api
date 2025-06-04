from django.db import models
from django.utils.text import slugify
import uuid
from api.models import Account
import secrets
# from .paystack import Paystack



class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # allow blank so we can auto fill
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')
    created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Product(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount_Price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='store')
    photoOne = models.ImageField(upload_to='store', null=True, blank=True)
    photoTwo = models.ImageField(upload_to='store', null=True, blank=True)
    photoThree = models.ImageField(upload_to='store', null=True, blank=True)
    photoFour  = models.ImageField(upload_to='store', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    in_stock = models.IntegerField()
    # product_id = models.UUIDField(unique=True, null=True, blank=True)
    product_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if not self.product_id:
    #         # self.product_id = uuid.uuid4(self.title)
    #         self.product_id = uuid.uuid4()
    #     super().save(*args, **kwargs)







class Cart(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    total = models.PositiveIntegerField()
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.account.username} - {str(self.total)}'


# cartProduct model

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    Amout = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    # remove = models.deletion()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'CartProduct - {self.cart.id} {self.quantity}'
    

ORDER_STATUS=(
    ('pending', 'pending'),
    ('complate', 'complate'),
    ('cancel', 'cancel'),
)

PAYMENT_METHOD=(
    ('paypal', 'paypal'),
)

class OrderProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_by = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    amount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    orderstatus = models.CharField(choices=ORDER_STATUS, default='pending')
    payment_method = models.CharField(choices=PAYMENT_METHOD, default='paypal')
    complete = models.BooleanField(default=False)
    ref = models.CharField(null=True, blank=True, unique=True)

    def __str__(self):
        return f'{self.amount} - {str(self.id)}'
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = OrderProduct.filter(ref = ref).exists()
            if not obj_with_sm_ref:
                self.ref = ref
            super().save(*args, **kwargs)

    # amount from cent/kobo to naira or dollars

    def amount_value(self)->int:
        return self.amount * 100
    
    # veridy_paymet
    def  verify_payment(self):
        paypal = paypal()
        status,result = paypal.verify_payment(self.ref)
        if status and result.get('status') == 'success':
            if result['amount']/100 == self.amount:
                self.payment_complete == True
                self.cart.delete
                self.save()
            return False
