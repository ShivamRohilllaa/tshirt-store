from django.contrib import admin
from .models import *

# Register your models here.

class SizeVariantConfig(admin.TabularInline):
    model = Sizevariant

class TshirtConfig(admin.ModelAdmin):
    inlines = [SizeVariantConfig]    



admin.site.register(Tshirt, TshirtConfig)
admin.site.register(Occassion)
admin.site.register(Sleeve_type)
admin.site.register(Neck_type)
admin.site.register(Ideal_for)
admin.site.register(brand)
admin.site.register(color)
admin.site.register(Payment)
admin.site.register(order)
admin.site.register(order_item)