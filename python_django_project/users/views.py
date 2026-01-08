from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


# Create your views here.
User = get_user_model()

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
      return redirect('accounts:dashboard')
    else:
      messages.error(request,'Invalid credentials')
      return redirect('accounts:login')
  else:
    return render(request,'accounts/login.html')
  
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
          return redirect('accounts:register')
        else: 
          if User.objects.filter(email=email).exists():
            messages.error(request,'Email already exists.')
            return redirect('accounts:register')
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
            return redirect('accounts:login')
      else:
        messages.error(request,'Password do not match.')
        return redirect('accounts:register')
    else:
      return render(request,'accounts/register.html')

def logout(request):
  if request.method=="POST":
    auth.logout(request)
    messages.success(request,'You are now logged out.')
    return redirect('pages:index')
  return redirect('pages:index')