from .models import Cart, Cart_item
from .views import cart_id


def counter(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=cart_id(request))
            cart_items = Cart_item.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                count += cart_item.quantity
        except Cart.DoesNotExist:
            count = 0
        return {'count': count}
