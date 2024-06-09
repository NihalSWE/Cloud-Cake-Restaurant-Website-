from django.db import models
from PIL import Image
from django.utils import timezone

# Create your models here.
CATEGORY_CHOICES=(
    ('B','Beard&Cookies'),
    ('C','Cake'),
    ('F','Frozen'),
    ('S','Savory'),
)

from django_ckeditor_5.fields import CKEditor5Field
from .utils import sanitize_html  # Import the sanitize_html function

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    detail = CKEditor5Field(config_name='default',max_length=1200,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, default='J', max_length=2)
    image = models.ImageField(upload_to="product_img")

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if self.detail:
            self.detail = sanitize_html(self.detail)  # Sanitize the detail field
        super(Product, self).save(*args, **kwargs)

    
    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            # Set the desired image size
            fixed_width = 1080
            fixed_height = 1080

            # Resize the image
            img = img.resize((fixed_width, fixed_height), Image.LANCZOS)
            img.save(self.image.path)
    

class AddCart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
     return str(self.id)

@property
def total_cost(self):
    return self.quantity * self.product.price



from django.contrib.postgres.fields import JSONField
class Order(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    address = models.TextField()
    cart_items = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Banner(models.Model):
    image = models.ImageField(upload_to='banners')  # Assuming the banner image is stored as an ImageField

    def __str__(self):
        return f'Banner {self.id}'  # Display the banner ID in the admin panel



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.timestamp}'