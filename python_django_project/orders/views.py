from django.shortcuts import render
from .models import Order
from carts.models import Cart
from cartitems.models import CartItem
from orderitems import OrderItem
# Create your views here.
def checkout(request,cart_id):
  cart = Cart.objects.get(card_id=cart_id)
  order = Order.objects.create(
    user = cart.user,
    total_price=calculate_total(cart),
    delivery_method='SF',
    status="Pending"
  )

  items = CartItem.objects.filter(cart=cart)
  for item in items:
      OrderItem.objects.create(
        order=order,
        product = item.product,
        price=item.product.price,
        quantity=item.quantity
      )
  
      item.product.stock_count -=item.quantity
      item.product.save()

  cart.products.clear()

def update_total_price(self):
    total=sum(item.price * item.quantity for item in self.items.all())
    self.total_price=total
    self.save()