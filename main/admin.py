from django.contrib import admin
from .models import Product, Cart
# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)

admin.site.site_header = 'CBC Administration'
admin.site.index_title = 'CBC Administration'
