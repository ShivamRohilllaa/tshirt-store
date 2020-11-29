from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
# Create your models here.

class Tshirtproperty(models.Model):
    title = models.CharField(max_length=50, null=False) 
    slug = AutoSlugField(populate_from='title', unique=True, null=False, default="")

    class Meta:
        abstract = True #This means this table is not created in the database

    def __str__(self):
        return self.title
        
class Occassion(Tshirtproperty):
    pass

class Sleeve_type(Tshirtproperty):
    pass
class Neck_type(Tshirtproperty):
    pass
class Ideal_for(Tshirtproperty):
    pass
class brand(Tshirtproperty):
    pass
class color(Tshirtproperty):
    pass

class Tshirt(models.Model):
    name = models.CharField(max_length=50, null=True)
    slug = AutoSlugField(populate_from='name', unique=True, null=False, default="")
    desc = models.CharField(max_length=50, null=True)
    discount = models.IntegerField(default=0)
    image1 = models.ImageField(upload_to='products', null=False)
    image2 = models.ImageField(upload_to='products', null=False)
    image3 = models.ImageField(upload_to='products', null=False)
    image4 = models.ImageField(upload_to='products', null=False)
    occassion = models.ForeignKey(Occassion, on_delete=models.CASCADE)
    sleeve = models.ForeignKey(Sleeve_type, on_delete=models.CASCADE)
    neck = models.ForeignKey(Neck_type, on_delete=models.CASCADE)
    ideal = models.ForeignKey(Ideal_for, on_delete=models.CASCADE)
    brand = models.ForeignKey(brand, on_delete=models.CASCADE)
    color = models.ForeignKey(color, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
class Sizevariant(models.Model):
    SIZES = (
        ('S', "Small"),
        ('M', "Medium"),
        ('L', "Large"),
        ('XL', "Extra Large"),
        ('XXL', "Extra Extra Large"),
    )
    price = models.IntegerField(null=False)
    tshirt = models.ForeignKey(Tshirt, on_delete=models.CASCADE)
    size = models.CharField(choices=SIZES, max_length=5)


class Cart(models.Model):
    sizevariant = models.ForeignKey(Sizevariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class order(models.Model):
    orderStatus = (
        ('PENDING', "Pending"),
        ('PLACED', "Your Order Is Placed"),
        ('CANCELED', "Your Order Is Canceled"),
        ('PACKED', "Your Order Is Packed"),
        ('SHIPPED', "Your Order Is Ready For Shipping"),
    )
    method = (
        ('COD', "Cod"),
        ('ONLINE', "Online"),
    )
    order_status = models.CharField(max_length=15, choices=orderStatus)
    payment_method = models.CharField(max_length=15, choices=method)
    shipping_address = models.CharField(max_length=150, null = False)
    phone = models.CharField(max_length=10, null = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)

    def __str__(self):
        return self.order_status



class order_item(models.Model):
    Order = models.ForeignKey(order, on_delete=models.CASCADE)
    tshirt = models.ForeignKey(Tshirt, on_delete=models.CASCADE)
    size = models.ForeignKey(Sizevariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)

class Payment(models.Model):
    Order = models.ForeignKey(order, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=15, default='FAILED')
    date = models.DateTimeField(null=False, auto_now_add=True)
    payment_id = models.CharField(max_length=70)
    payment_request_id = models.CharField(max_length=70, unique=True, null = False)




