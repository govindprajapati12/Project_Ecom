from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from products.models import * 
from django.contrib.auth import login, authenticate,logout,get_user_model
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
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
def home_view(request):
    categories = Category.objects.all()  # Fetch all categories from database
    
    context = {
        'categories': categories,  # Pass categories to the template context
    }
    return render(request, 'home.html', context)
def home_page(request):
    category_data=Category.objects.all()

    context={
        'category_data':category_data,

    }
    # print(context,"-------------------------")

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

def search_categories(request):
    query = request.GET.get('query')
    c_id = request.GET.get('c_id')

    if c_id:
        categories = Category.objects.filter(pk=c_id)
    elif query:
        categories = Category.objects.filter(c_name__icontains=query)
    else:
        categories = Category.objects.all()

    context = {
        'categories': categories,
        'query': query,
    }
    return render(request, 'search_results.html', context)
def products(request, c_id):
    category = Category.objects.get(pk=c_id)
    products = category.products.all()
    # categories = Category.objects.all()
    context = {
        'category': category,
        'products': products,
        # 'categories': categories  # Pass categories to context
    }
    return render(request, 'products.html', context)


def product_detail(request, product_id,c_id):
    product = get_object_or_404(Product, p_id=product_id)
    category = Category.objects.get(pk=c_id)
    # products = category.products.all()
    similar_products = category.products.exclude(p_id=product_id)
    # print(category)
    # print(products)
    
    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
    else:
        form = QuantityForm(initial={'quantity': 100}) 
    
    context = {
        'product': product,
        'form': form,
        'similar_products': similar_products,
        'category': category,
    }
    return render(request, 'product_detail.html',context)
def filter_products(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    c_id = request.GET.get('c_id', None)
    
    products = Product.objects.all()
    
    if c_id:
        try:
            category = Category.objects.get(pk=c_id)
            products = products.filter(c_id=category)
        except Category.DoesNotExist:
            pass
    
    if min_price:
        products = products.filter(p_price__gte=min_price)
    if max_price:
        products = products.filter(p_price__lte=max_price)
    
    context = {
        'products': products,
        'category': category if 'category' in locals() else None,
    }
    return render(request, 'products.html', context)
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

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
    return redirect('home_view')  # Redirect to the home page after logging out

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('home_view')  # Replace 'home' with your desired redirect URL after account deletion
    return render(request, 'profile.html')  # Replace 'profile.html' with your actual profile page template
# def get_cart_items(user):
    # return Cart.objects.filter(user=user)

@login_required
def generate_quotation(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_amount = sum(item.product.p_price * item.quantity for item in cart_items)
    
    quotation = Quotation.objects.create(user=user, total_amount=total_amount)
    
    for item in cart_items:
        QuotationItem.objects.create(
            quotation=quotation,
            product_name=item.product.p_name,
            quantity=item.quantity,
            unit_price=item.product.p_price,
            total_price=item.product.p_price * item.quantity
        )
    
    # Send email with quotation details
    send_quotation_email(user, quotation)
    
    # Clear the cart after successful quotation generation
    cart_items.delete()
    
    return redirect('view_quotation', quotation_id=quotation.id)

def send_quotation_email(user, quotation):
    subject = 'Your Travel Crafters Quotation'
    from_email = 'TravelCrafters10@gmail.com'
    to_email = [user.email]
    
    # Render email content from template
    html_content = render_to_string('quotation_email.html', {'user': user, 'quotation': quotation})
    text_content = strip_tags(html_content)  # Strip HTML tags for the plain text email
    
    # Send email
    send_mail(subject, text_content, from_email, to_email, html_message=html_content)

@login_required
def view_quotation(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    return render(request, 'quotation.html', {'quotation': quotation}) 

@login_required
def my_quotations(request):
    user = request.user
    quotations = Quotation.objects.filter(user=user)
    return render(request, 'my_quotations.html', {'quotations': quotations})


@login_required
def place_order(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    cart_items = Cart.objects.filter(user=request.user)
    admin_user = User.objects.first()  # Assuming the first user is the admin; adjust as necessary
    
    if not admin_user:
        return redirect('view_quotation', quotation_id=quotation.id)

    try:
        with transaction.atomic():
            # Create the Order instance
            order = Order.objects.create(
                user=request.user,
                quotation=quotation,
                business_contact_name=admin_user.username,
                business_contact_number=admin_user.phone_number  # Adjust to match your custom user field
            )

            # Create OrderItem instances for each cart item
            for cart_item in cart_items:
                total_price = cart_item.product.p_price * cart_item.quantity  # Calculate total price
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.product.p_price,
                    total_price=total_price  # Save calculated total price
                )

            # Clear the cart after successful order placement
            cart_items.delete()

            # Send confirmation email
            html_content = render_to_string('order_confirmation_email.html', {
                'user': request.user,
                'order': order,
                'order_items': OrderItem.objects.filter(order=order),
                'total_price': sum(item.total_price for item in OrderItem.objects.filter(order=order)),
                'business_contact_name': admin_user.username,
                'business_contact_number': admin_user.phone_number,
            })

            send_mail(
                subject='Order Confirmation from Travel Crafters',
                message='',
                from_email='TravelCrafters10@gmail.com',
                recipient_list=[request.user.email],
                fail_silently=False,
                html_message=html_content,
            )

            messages.success(request, 'Your order has been placed successfully and a confirmation email has been sent.')

            # Redirect to view the order details
            return redirect('view_order', order_id=order.id)

    except Exception as e:
        # Handle any exceptions or rollback if necessary
        print(f"Error placing order: {e}")
        return redirect('view_quotation', quotation_id=quotation.id)

@login_required
def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    total_price = sum(item.total_price for item in order_items)
    return render(request, 'view_order.html', {'order': order, 'order_items': order_items, 'total_price': total_price})

@login_required
def myorder_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'myorder_list.html', {'orders': orders})


