from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart
from cartitems.models import CartItem
from products.models import Product

# Create your views here.
def _get_or_create_cart(request):
  if request.user.is_authenticated:
    cart,_ = Cart.objects.get_or_create(user=request.user)
  else:
    if not request.session.session_key:
      request.session.create()

    session_id=request.session.session_key
    cart,_=Cart.objects.get_or_create(session_id=session_id,user=None)
  return cart

# @login_required
def api_add_to_cart(request,product_id):
  if request.method == "POST":
    product = get_object_or_404(Product,id=product_id)
    cart = _get_or_create_cart(request)

    size = request.POST.get('size','Standard')

    item , created = CartItem.objects.get_or_create(cart=cart , product=product,size=size)

    print(f"DEBUG: Cart ID is {cart.id}")
    print(f"DEBUG: Item created: {created}, Quantity: {item.quantity}")
    if not created:
      item.quantity+=1
    else:
      item.quantity=1
    item.save()

    cartitem_set = CartItem.objects.filter(cart=cart).count()
    # return JsonResponse({"status": "success","message":"Added to cart"})
    print(f"Items in cart: {cartitem_set}")
    return redirect(request.META.get('HTTP_REFERER','products:index'))
  # return redirect('products:index')
  return redirect('carts:view_cart')

# @login_required
def api_update_cart_item(request,item_id):
  cart = _get_or_create_cart(request)

  item = get_object_or_404(CartItem , id = item_id,cart=cart)
  action = request.POST.get('action')

  if action == 'increase':
    item.quantity+=1
  elif action == 'decrease' and item.quantity>1:
    item.quantity -=1

  item.save()
  # return JsonResponse({'status':'success', 'new_quantity' : item.quantity})
  return redirect('carts:view_cart')

# @login_required
def remove_from_cart(request,item_id):
  cart = _get_or_create_cart(request)
  cart_item = get_object_or_404(CartItem,id=item_id,cart=cart)

  cart_item.delete()
  return redirect('carts:view_cart')
  
# @login_required
def view_cart(request):
  cart= _get_or_create_cart(request)
  cart_items = CartItem.objects.filter(cart=cart)
  total_price = sum(item.product.price * item.quantity for item in cart_items)

  context = {'cart':cart,
              'cart_items':cart_items ,
              'total_price':total_price}
  return render(request,'carts/cart_detail.html',context)

# get_object_or_404(CartItem, id=item_id), 仆街user random試一個id,就可以delete/modify其他user既shopping cart
# 加cart＝cart , system會check this ID is it in your cart 