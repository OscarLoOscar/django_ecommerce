from django.shortcuts import render ,get_object_or_404
from .models import Product
from categories.models import Category

# Create your views here.
def product_list(request):
  products = Product.objects.filter(is_published=True)
  categories = Category.objects.all().order_by('order')

  category_id = request.GET.get('category')
  if category_id:
    products = products.filter(category_id = category_id)

  context = {'products': products,'categories':categories}
  return render(request,'products/product_list.html',context)

def product_detail(request,pk):
  product = get_object_or_404(Product,pk=pk)
  return render(request,'products/product_detail.html',{'product':product})
