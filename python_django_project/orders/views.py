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

def get_subtotal(cart_items):
   return sum(item.product.price * item.quantity for item in cart_items)

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

@login_required
@transaction.atomic # Prevent Rollback
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)

    if request.method == 'POST':
      if not cart_items.exists():
        messages.error(request,"你的購物車係空的")
        return redirect('products:product_list')
      
      total_amount = get_subtotal(cart_items)

      try:
        order = Order.objects.create(
          user = request.user,
          total_price=total_amount,
          delivery_method=request.POST.get('delivery_method'),
          payment_method=request.POST.get('payment_method'),
          shipping_location = request.POST.get('shipping_location',''),
          sf_region = request.POST.get('sf_region',''),
          sf_address = request.POST.get('sf_address',''),
          status="Pending"
        )

        for item in cart_items:
          if item.product.stock_count < item.quantity:
              messages.error(request,f"產品{item.product.title} 庫存不足")
              raise Exception(f"產品{item.product.title} 庫存不足")
      
          OrderItem.objects.create(
            order=order,
            product = item.product,
            price=item.product.price,
            quantity=item.quantity,
            size=item.size
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
      except Exception as e:
        messages.error(request,str(e))
        return redirect('carts:view_cart')
      
    context = {
      'cart_items':cart_items,
      'total_price': get_subtotal(cart_items),
    }
    return render(request,'orders/checkout.html', context)

