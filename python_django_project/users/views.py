from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from orders.models import Order
from users.models import PurchaseHistory
from django.http import JsonResponse
# Create your views here.
User = get_user_model()

# @login_required
def login(request):
  if request.method == "POST":
    username_input = request.POST.get('username') # username = username / email , username is variable
    password_input = request.POST.get('password')

    user = auth.authenticate(request,
                            username=username_input,
                            password=password_input)

    if user is not None:
      auth.login(request,user)
      messages.success(request,'You are now logged in.')
      # react change
      return redirect('users:dashboard')
    else:
      messages.error(request,'Invalid credentials')
      return redirect('users:login')
  else:
    return render(request,'users/login.html')
  
def register(request):
    if request.method == "POST":
      username = request.POST.get('username')
      password = request.POST.get('password')
      first_name = request.POST.get('first_name')
      last_name = request.POST.get('last_name')
      email = request.POST.get('email')
      password = request.POST.get('password')
      password2 = request.POST.get('password2')
      phone = request.POST.get('phone')

      if password == password2:
        if User.objects.filter(username=username).exists():
          messages.error(request,'Username already exists.')
          return redirect('users:register')
        else: 
          if User.objects.filter(email=email).exists():
            messages.error(request,'Email already exists.')
            return redirect('users:register')
          else:
            user=User.objects.create_user(
              username=username,
              password=password,
              email=email,
              first_name=first_name,
              last_name=last_name,
              phone=phone
            )
            messages.success(request,'You are now registered and can login.')
            return redirect('users:login')
      else:
        messages.error(request,'Password do not match.')
        return redirect('users:register')
    else:
      return render(request,'users/register.html')

@login_required
def logout(request):
  if request.method=="POST":
    auth.logout(request)
    messages.success(request,'You are now logged out.')
    return redirect('pages:index')
  return redirect('pages:index')

@login_required
def dashboard(request):
  orders = Order.objects.filter(user=request.user).order_by('-created_at')
  purchase_history = PurchaseHistory.objects.filter(user=request.user).select_related('product')

  context = {
    'orders':orders,
    'purchase_history':purchase_history,
  }

  return render(request,'users/dashboard.html',context)
  # order_list = [{
  #   'id':order.id,
  #   'total':float(order.total_price),
  #   'status':order.status,
  #   'date':order.created_at.strftime('%Y-%m-%D %H:%M')
  # } for order in orders]

  # return JsonResponse({
  #   'username':request.user.username,
  #   'orders':order_list,
  #   'history_count':purchase_history.count()
  # })