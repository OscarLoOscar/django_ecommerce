from django.shortcuts import render
from products.models import Product
from django.http import HttpResponse
# Create your views here.
def index(request):
  # products = product.objects.all() # 大階Listing，拎data model，all() -> 同DB溝通，拎晒所有data
  product_list = Product.objects.filter(is_published=True)[:3] # [:3] -> list -> 0,1,2 , .order_by('-list_date')
  context = {
    'product_list' : product_list,
    # 'district_groups_choices': district_groups_choices,
    # 'bedroom_choices':bedroom_choices,
    # 'room_type_choices':room_type_choices
}
#   # return render(request,'pages/index.html',{'anything' : 'something','numbers': 1234})
  return render(request,'pages/index.html',context) # 之後會多database，但煩，難改，方便加model

def about(request):
  # return HttpResponse('<h1>about</h1>')
  # doctors = Doctor.objects.order_by('-hire_date')[:3]
  is_published = Product.objects.all()
  context = {"is_published":is_published}
  return render(request,'pages/about.html',context)

def contact(request):
  return render(request,'pages/contact.html')