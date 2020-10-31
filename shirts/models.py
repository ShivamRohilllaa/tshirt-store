from django.db import models
from autoslug import AutoSlugField
# Create your models here.

class Tshirtproperty(models.Model):
    title = models.CharField(max_length=50, null=False) 
    slug = models.CharField(max_length=50, unique=True)

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
