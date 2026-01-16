from .views import _get_or_create_cart
from cartitems.models import CartItem

def cart_renderer(request):
  try:
    cart = _get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return {
      'global_cart_items': cart_items,
      'global_cart_total': total_price,
      'global_cart_count':cart_items.count()
    }
  except:
    return {'global_cart_items':[],'global_cart_total':0,'global_cart_count':0}