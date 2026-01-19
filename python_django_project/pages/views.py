from django.shortcuts import render,redirect
from products.models import Product
from django.contrib import messages
from django.http import HttpResponse
from .models import ContactMessage 
# Create your views here.
def index(request):
  # products = product.objects.all() # 大階Listing，拎data model，all() -> 同DB溝通，拎晒所有data
  all_product = Product.objects.filter(is_published=True)[:3] # [:3] -> list -> 0,1,2 , .order_by('-list_date')
  context = {
    'all_product' : all_product,
    # 'district_groups_choices': district_groups_choices,
    # 'bedroom_choices':bedroom_choices,
    # 'room_type_choices':room_type_choices
}
#   # return render(request,'pages/index.html',{'anything' : 'something','numbers': 1234})
  print(f"DEBUG: Found {all_product.count()} products.")
  return render(request,'pages/index.html',context) # 之後會多database，但煩，難改，方便加model

def about(request):
  # return HttpResponse('<h1>about</h1>')
  # doctors = Doctor.objects.order_by('-hire_date')[:3]
  is_published = Product.objects.all()
  context = {"is_published":is_published}
  return render(request,'pages/about.html',context)

def contact_view(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    message_content = request.POST.get('message')

    if not name or not email or not message_content:
      messages.error(request,"請填寫所有必填欄位")
      return render(request,'pages/contact.html')
    contact_record = ContactMessage(
      name=name,
      email=email,
      subject=subject,
      message=message_content
    )

    if request.user.is_authenticated:
      contact_record.user = request.user

    contact_record.save()

    return redirect('pages:contact_success')
  return render(request,'pages/contact.html')

def contact_success(request):
  return render(request,'pages/contact_success.html')

def privacypolicy(request):
  return render(request,'pages/privacy_policy.html')

def tandc(request):
  return render(request,'pages/terms_and_conditions.html')