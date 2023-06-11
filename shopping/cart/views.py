from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, Cart_item
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
    except ObjectDoesNotExist:
        cart = Cart.objects.create(cart_id=cart_id(request))
        cart.save()

    try:
        cart_item = Cart_item.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()

    except ObjectDoesNotExist:
        cart_item = Cart_item.objects.create(product=product, cart=cart, quantity=1)
        cart_item.save()

    return redirect('cart:cart_details')


def cart_details(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_items = Cart_item.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', {'cart_item': cart_items, 'counter': counter, 'total': total})


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cart_item.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_details')


def remove(request, product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cart_item.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart:cart_details')
