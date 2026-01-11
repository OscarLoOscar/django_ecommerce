from django.shortcuts import render ,get_object_or_404
from .models import Product
from categories.models import Category
from django.db.models import Q
from django.http import JsonResponse
# Create your views here.
def product_list(request):
  products = Product.objects.filter(is_published=True)
  categories = Category.objects.all().order_by('order')

  query = request.GET.get('q')
  if query:
    products = products.filter(
      Q(title__icontains=query) |Q(description__icontains=query)
    )


  category_id = request.GET.get('category')
  if category_id:
    products = products.filter(category_id = category_id)

  # django html
  # categories = Category.objects.all().order_by('order')
  context = {'products': products,
              'categories':categories,
              'query':query}
  return render(request,'products/product_list.html',context)

  # data = [{
  #   "id":p.id,
  #   "title":p.title,
  #   "price":float(p.price),
  #   "image":p.image.url if p.image else ""
  # } for p in products]

  # return JsonResponse({'products':data})

def product_detail(request,pk):
  product = get_object_or_404(Product,pk=pk)
  return render(request,'products/product_detail.html',{'product':product})
