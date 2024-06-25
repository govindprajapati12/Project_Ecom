from django.contrib import admin
from .models import Category, Product, Material, ProductMaterial, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra forms in the inline

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Material)
admin.site.register(ProductMaterial)
