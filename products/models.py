from django.db import models
from tinymce.models import HTMLField
from app.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.


class Category(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=255)
    c_details = HTMLField()
    c_image = models.ImageField(upload_to='category_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.c_name


class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    c_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    p_name = models.CharField(max_length=255)
    p_price = models.IntegerField()
    p_details =HTMLField()
    p_image = models.ImageField(upload_to='product_images/',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.p_name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"{self.product.p_name} Image"

class Material(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_name = models.CharField(max_length=255)
    m_description =HTMLField()
    m_image = models.ImageField(upload_to='material_images/')
    m_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.m_name
 

class ProductMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    p_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_materials')
    m_id = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='material_products')

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming Product is another model
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart #{self.id} - {self.user.username} - {self.product.p_name}"
    



class Quotation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Quotation {self.id} for {self.user}"

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product_name} - {self.quotation}"
    


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    quotation = models.OneToOneField(Quotation, on_delete=models.CASCADE, null=True, blank=True)
    business_contact_name = models.CharField(max_length=100)
    business_contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem #{self.id} - Order #{self.order.id} - {self.product.p_name}"
    