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

    STATUS_CHOICES = [
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancel', 'Cancel'),
    ]

    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    cart_items = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # New status field with choices
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Processing'
    )

    def __str__(self):
        return f"Order {self.id} - {self.status}"

# models.py
from django.db import models
from django.contrib.auth.models import User






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
    


class Outlet(models.Model):
    title = models.CharField(max_length=100)
    map_iframe = models.TextField(null=True)  # Store the full iframe HTML here
    address = models.TextField(null=True)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='outlet_images/', null=True, blank=True)  # New field for the outlet image

    def __str__(self):
        return self.title
    

class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

from django.db import models

class Designation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Career(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    email = models.EmailField(null=True)
    address = models.CharField(max_length=255, null=True)
    message = models.TextField(null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE,null=True)
    cv = models.FileField(upload_to='cv_uploads/%Y/%m/%d/')
    submitted_at = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.name



class CategoryImage(models.Model):
    CATEGORY_CHOICES = [
        ('cake', 'Cake'),
        ('bread', 'Bread'),
        ('savory', 'Savory'),
        ('frozen', 'Frozen'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.category 
    


class FoodItems(models.Model):
    name = models.CharField(max_length=100)
    mrp = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
from django.db import models




from django.db import models



class AboutUs(models.Model):
    story = models.TextField(max_length=500)
    story_image = models.ImageField(upload_to='about/', blank=True, null=True)
    mission = models.TextField(max_length=500)
    mission_image = models.ImageField(upload_to='about/', blank=True, null=True)

    def __str__(self):
        return "About Page Content"
class AboutUs_TeamMember(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/')

    def __str__(self):
        return self.name