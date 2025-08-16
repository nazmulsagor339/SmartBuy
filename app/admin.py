from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Customer,
    Product,
    Cart,
    Order
)
# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','city','district','zipcode']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id','customer','user','customerInfo','product','productInfo','quantity','ordered_date','status']

    def customerInfo(self,obj):
        # admin:appName_modelName_change
        info = reverse("admin:app_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',info,obj.customer.name)
    
    def productInfo(self,obj):
        # admin:appName_modelName_change
        info = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',info,obj.product.title)