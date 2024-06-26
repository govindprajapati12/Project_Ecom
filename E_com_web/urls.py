"""
URL configuration for E_com_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

from django.conf import settings

from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name="home_view"),
    path('categories/',views.home_page,name="home_page"),

    path('contact_page/',views.contact ,name="contact_page"),
    path('aboout_page/',views.about ,name="about_page"),
    path('sign_in/',views.sign_in,name="sign_in_page"),
    path('sign_up/', views.sign_up, name="sign_up_page"),
    # path('my_order/', views.order, name="myorder_page"),
    path('profile/', views.profile_view, name="profile_page"),
    # path('cart/', views.cart, name="cart_page"),
    path('logout/', views.logout_view, name='logout'),
    path('products/<int:c_id>/', views.products, name='products_page'),
    path('products/', views.products, name='products'),
 
    
    # path('profile/', views.profile, name='profile'),
    path('product/<int:product_id><int:c_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('generate_quotation/', views.generate_quotation, name='generate_quotation'),
    path('quotation/<int:quotation_id>/', views.view_quotation, name='view_quotation'),
    path('place_order/<int:quotation_id>/', views.place_order, name='place_order'),
    path('order/<int:order_id>/', views.view_order, name='view_order'),
    path('oders_detail/',views.myorder_list,name='myorder_list'),
    


    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
