from django.db import models

# Create your models here.
CATEGORY_CHOICES=(
    ('B','Beard&Cookies'),
    ('C','Cake'),
    ('F','Frozen'),
    ('S','Savory'),
)

class Product(models.Model):
    title=models.CharField(max_length=100)
    price=models.FloatField()
    discount_price=models.FloatField(blank=True,null=True)
    detail=models.TextField(max_length=200,null=True)
    category=models.CharField(choices=CATEGORY_CHOICES,default='J',max_length=2)
    image=models.ImageField(upload_to="product_img")

    def __str__(self):
        return str(self.id)
    

class AddCart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
     return str(self.id)

@property
def total_cost(self):
    return self.quantity * self.product.price



from django.contrib.postgres.fields import JSONField
class Contact(models.Model):
    name=models.CharField(max_length=100)
    number=models.CharField(max_length=100)
    address=models.TextField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    cart_items = models.JSONField(null=True, blank=True)
    

    def __str__(self):
        return self.Name