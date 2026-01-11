from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order
from carts.models import Cart
from cartitems.models import CartItem
from orderitems.models import OrderItem
from users.models import PurchaseHistory
# Create your views here.

def calculate_total(cart_items):
   return sum(item.product.price * item.quantity for item in cart_items)

@login_required
@transaction.atomic # Prevent Rollback
def checkout(request):
    cart = get_object_or_404(Cart,user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items:
      messages.error(request,"你的購物車係空的")
      return redirect('products:product_list')
  
    if request.method == "POST":
      total_amount = calculate_total(cart_items)

      order = Order.objects.create(
        user = request.user,
        total_price=total_amount,
        delivery_method=request.POST.get('delivery_method'),
        payment_method=request.POST.get('payment_method'),
        status="Pending"
      )

      for item in cart_items:
        if item.product.stock_count < item.quantity:
            messages.error(request,f"產品{item.product.title} 庫存不足")
            raise Exception("庫存不足")
      
        OrderItem.objects.create(
          order=order,
          product = item.product,
          price=item.product.price,
          quantity=item.quantity
        )
  
        PurchaseHistory.objects.get_or_create(
            user=request.user,
            product=item.product
        )

        item.product.stock_count -=item.quantity
        item.product.save()

      # cart.products.clear()
        cart_items.delete()

      messages.success(request,f"訂單 #{order.id} 已建立，請盡快付款")
      return redirect('users:dashboard')
    return render(request,'orders/checkout.html', {'total_price': calculate_total(cart_items)})

# def update_total_price(self):
#     total=sum(item.price * item.quantity for item in self.items.all())
#     self.total_price=total
#     self.save()

@login_required
def simulate_sample(request,order_id):
  # mock paid success payment
  order = get_object_or_404(Order,id=order_id,user=request.user)
  order.status = "Paid"
  order.save()

  messages.success(request,'付款成功！確認信已寄往你嘅 Email。')
  return redirect('users:dashboard')