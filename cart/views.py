from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from onlineshop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, ClientForm
from .models import Client, Order, OrderItem

# Add product to cart
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')

# Remove product from cart
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

# Display cart details
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})

# Checkout View (Collects Client Information and Saves Order)
@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            # Get or create the client based on the user
            client, created = Client.objects.get_or_create(user=request.user, defaults=form.cleaned_data)
            
            # Create an order with the total price calculated
            order = Order.objects.create(client=client, total_price=sum(item['price'] * item['quantity'] for item in cart))
            
            # Add items to the order
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product_name=item['product'].name,
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Clear the cart after placing the order
            cart.clear()
            # Redirect to the order success page
            return redirect('cart:order_success')

    else:
        # If GET request, show the checkout form
        form = ClientForm()

    return render(request, 'cart/checkout.html', {'cart': cart, 'form': form})

# Order Success View (Displayed After Successful Order)
def order_success(request):
    return render(request, 'cart/order_success.html')
