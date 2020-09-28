from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Product, Cart, Order
from .forms import ProductForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def showProducts(request):
    products = Product.objects.all()
    user_count = User.objects.count()
    product_count = Product.objects.count()
    context = {
        'products' : products,
        'u_c' : user_count,
        'p_c' : product_count
    }
    return render(request, 'ProductManagement/products.html', context)


def showDetails(request, product_id):
    searched_product = get_object_or_404(Product, id=product_id)
    context = {
        'search': searched_product
    }

    return render(request, 'ProductManagement/detail_product_view.html', context)

@login_required
def uploadProducts(request):
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid:
            form.save()
            return redirect('products_list')

    context = {
        'form' : form
    }

    return render(request, 'ProductManagement/upload.html', context)


@login_required
def view_cart(request):
    cart = Cart(user=request.user)
    try:
        cart = Cart.objects.get(user=request.user)
    except cart.DoesNotExist:
        cart = Cart(user=request.user)
        cart.save()

    total = 0
    for product in cart.product.all():
        total += product.price

    context = {
        'cart': cart,
        'total' : total
    }

    return render(request, 'ProductManagement/cart.html', context)

@login_required
def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    #cart = get_object_or_404(Cart, user = request.user)

    try:
        cart = Cart.objects.get(user=request.user)
    except cart.DoesNotExist:
        cart = Cart(user=request.user)

    cart.product.add(product)
    cart.save()


    #return HttpResponseRedirect(reverse('cart'))
    return redirect('cart')

@login_required
def delete_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user)

    cart.product.remove(product)
    cart.save()

    return redirect('cart')

@login_required
def my_orders(request):

    order_status = True
    orders = Order(user=request.user)

    try:
        orders = Order.objects.filter(user=request.user)
    except orders.DoesNotExist:
        orders = Order(user=request.user)
        order_status = False

    total = 0.0
    for order in orders:
        total += order.product.price


    context = {
        'orders': orders,
        'order_status': order_status,
        'total' : total

    }

    return render(request, 'ProductManagement/order.html', context)


@login_required
def make_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    order = Order(user=request.user, product=product)
    order.save()

    cart = Cart.objects.get(user=request.user)
    cart.product.remove(product)
    cart.save()

    #return HttpResponseRedirect(reverse('cart'))
    return redirect('cart')

