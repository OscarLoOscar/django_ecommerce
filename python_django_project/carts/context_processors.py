from .views import _get_or_create_cart
from cartitems.models import CartItem

def cart_render(request):
  try:
    cart = _get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return {
      'global_cart_items': cart_items,
      'global_cart_total': total_price,
      'global_cart_count': sum(item.quantity for item in cart_items)
    }
  except Exception as e:
    return {'global_cart_items':[],'global_cart_total':0,'global_cart_count':0}