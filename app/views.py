from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from products.models import * 
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm, SignInForm,ProfileUpdateForm
# from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import User
from django.core.mail import send_mail
# from .models import UserProfile
from .forms import QuantityForm
# Create your views here.
def home_view(request):
    return render(request,"home.html")
def home_page(request):
    category_data=Category.objects.all()
    context={
        'category_data':category_data,
    }
    print(context,"-------------------------")

    return render(request,"index.html",context)

def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home_page')  # Redirect to the profile page after saving
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def products(request, c_id):
    category = Category.objects.get(pk=c_id)
    products = category.products.all()
    categories = Category.objects.all()
    context = {
        'category': category,
        'products': products,
        'categories': categories  # Pass categories to context
    }
    return render(request, 'products.html', context)


def product_detail(request, product_id,c_id):
    product = get_object_or_404(Product, p_id=product_id)
    category = Category.objects.get(pk=c_id)
    products = category.products.all()
    print(category)
    print(products)
    
    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # Handle adding to cart logic here
    else:
        form = QuantityForm(initial={'quantity': 100})
    
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'product_detail.html',context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 100))

        # Get or create the cart for the current user and product
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)

        # Update quantity and total price in the cart
        if not created:
            cart.quantity += quantity
        else:
            cart.quantity = quantity

        cart.save()

        # Redirect to the cart view after adding/updating the cart item
        return redirect('cart_view')

    # Handle GET request or any other cases (though POST is expected for adding to cart)
    return redirect('product_detail', product_id=product_id)


@login_required
def cart_view(request):
    # Get the cart items for the current user
    cart_items = Cart.objects.filter(user=request.user)

    # Calculate total price for each item and the overall total price
    for item in cart_items:
        item.total_price = item.product.p_price * item.quantity

    total_price = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id, user=request.user)
    
    # Delete the cart item
    cart_item.delete()

    return redirect('cart_view')

@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 100))
        if quantity > 50:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove item if quantity is zero or negative

        return redirect('cart_view')

    return redirect('cart_view')


def sign_in(request):
    if request.method == 'POST':

        form = SignInForm(request, data=request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home_page')
            else:
                messages.error(request, "Invalid or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = SignInForm()
    return render(request, 'sign_in.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. Please sign in.')
            send_mail(
                'Welcome to Travel Crafters!',
                f'Dear {user.username},\n\n'
                'Thank you for connecting with us at Travel Crafters! We are delighted to welcome you to our community. '
                'As a valued member, you will be the first to hear about our latest products, exclusive offers, and special promotions. '
                'At Travel Crafters, we specialize in crafting high-quality corporate bags designed to meet your professional needs. '
                'Our commitment to excellence ensures that you receive products that are not only stylish but also durable and functional.\n\n'
                'Best regards,\n'
                'The Travel Crafters Team',
                'TravelCrafters10@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('sign_in_page')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect('home_page')  # Redirect to the home page after logging out