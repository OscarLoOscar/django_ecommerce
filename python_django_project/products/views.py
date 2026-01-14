from django.shortcuts import render ,get_object_or_404
from .models import Product
from categories.models import Category
from django.db.models import Q
from django.http import HttpResponse
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

def search(request):
  queryset_list = Product.objects.filter(is_published=True).order_by('-created_at')

  if'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(title__icontains=keywords)
  
  if'category' in request.GET:
    category_id = request.GET['category']
    if category_id:
      queryset_list = queryset_list.filter(category_id=category_id)

  query_data = request.GET.copy()
  if query_data.get('category'):
    try:
      query_data['category'] = int(query_data['category'])
    except ValueError:
      pass
    
  # if'price' in request.GET:
  #   price = request.GET['price']
  #   if price:
  #     queryset_list = queryset_list.filter(price__lte=price)

  # if'stock_count' in request.GET:
  #   stock = request.GET['stock_count']
  #   if stock:
  #     queryset_list = queryset_list.filter(stock_count__gte=stock)

  # if'size' in request.GET:
  #   size = request.GET['size']
  #   if size:
  #     queryset_list = queryset_list.filter(size=size)
  
  categories = Category.objects.all()

  context = {
    'products': queryset_list,
    'categories':categories,
    'values' : query_data
  }

  return render(request,'products/search.html',context)