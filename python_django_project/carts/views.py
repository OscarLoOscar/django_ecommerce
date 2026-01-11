from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart
from cartitems.models import CartItem
from products.models import Product

# Create your views here.
# @login_required
# def api_cart_detail(request):
#   cart, _ = Cart.objects.get_or_create(user=request.user)
#   cart_items = CartItem.objects.filter(cart=cart)
#   item_data = [{
#     "id":cart_items.id,
#     "product_id" : cart_items.product.id,
#     "title" : cart_items.product.title,
#     "price" : float(cart_items.product.price),
#     "quantity":cart_items.quantity,
#     "total" : float(cart_items.product.price),
#     "image" : cart_items.product.image.url if cart_items.product.image else ""
#   } for cart_item in cart_items]

#   return JsonResponse({
#     "items" : item_data,
#     "grant_total":sum(i["total"] for i in item_data)
#     })

@login_required
def api_add_to_cart(request,product_id):
  product = get_object_or_404(Product,id=product_id)
  cart, _ = Cart.objects.get_or_create(user=request.user)
  item , created = CartItem.objects.get_or_create(cart=cart , product=product)

  if not created:
    item.quantity+=1
  else:
    item.quantity=1
  item.save()

  # return JsonResponse({"status": "success","message":"Added to cart"})
  return redirect('carts:view_cart')

@login_required
def api_update_cart_item(request,item_id):
  item = get_object_or_404(CartItem , id = item_id,cart__user= request.user)
  action = request.POST.get('action')

  if action == 'increase':
    item.quantity+=1
  elif action == 'decrease' and item.quantity>1:
    item.quantity -=1

  item.save()
  # return JsonResponse({'status':'success', 'new_quantity' : item.quantity})
  return redirect('carts:view_cart')

@login_required
def remove_from_cart(request,item_id):
  cart_item = get_object_or_404(CartItem,id=item_id,cart__user=request.user)
  cart_item.delete()
  return redirect('carts:view_cart')
  
@login_required
def view_cart(request):
  cart, _ =Cart.objects.get_or_create(user=request.user)
  cart_items = CartItem.objects.filter(cart=cart)
  total_price = sum(item.product.price * item.quantity for item in cart_items)

  context = {'cart':cart,
              'cart_items':cart_items ,
              'total_price':total_price}
  return render(request,'carts/cart_detail.html',context)
