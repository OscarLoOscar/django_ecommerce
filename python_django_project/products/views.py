from django.shortcuts import render ,get_object_or_404
from .models import Product
from cartitems.models import CartItem
from categories.models import Category
from django.db.models import Q
from django.core.paginator import Paginator
from carts.views import _get_or_create_cart
# Create your views here.
def product_list(request):
  categories_list = ['耳環', '戒指', '手鏈', '頸鏈', '媽媽勾織']
  current_category_name = request.GET.get('category_type')

  products_list = Product.objects.filter(is_published=True).order_by('-created_at')
  categories = Category.objects.all().order_by('order')

  query = request.GET.get('q')
  if query:
    products_list = products_list.filter(
      Q(title__icontains=query) |Q(description__icontains=query)
    )

  category_id = request.GET.get('category')
  if category_id:
    products_list = products_list.filter(category_id = category_id)

  if current_category_name:
    products_list = products_list.filter(category__category_type=current_category_name)

  # Paginator
  paginator = Paginator(products_list,3)
  page = request.GET.get('page')
  products = paginator.get_page(page) # direct use for template

  # django html
  context = {'products': products,
              'categories':categories,
              'query':query,
              'categories_list':categories_list,
              'current_category':current_category_name,
            }
  return render(request,'products/product_list.html',context)

  # data = [{
  #   "id":p.id,
  #   "title":p.title,
  #   "price":float(p.price),
  #   "image":p.image.url if p.image else ""
  # } for p in products]

  # return JsonResponse({'products':data})

# 要跟products/urls.py 既setting ,用product_id ，但reference可以用pk/id
def product_detail(request,product_id):
  product = get_object_or_404(Product,pk=product_id)
  cart = _get_or_create_cart(request)

  cartitem_count = CartItem.objects.filter(cart=cart).count()

  context={
    'product':product,
    'cartitem_count':cartitem_count,
  }
  return render(request,'products/product_detail.html',context)

# def search(request):
  # queryset_list = Product.objects.filter(is_published=True).order_by('-created_at')
  
  # if'keywords' in request.GET:
  #   keywords = request.GET['keywords']
  #   if keywords:
  #     queryset_list = queryset_list.filter(title__icontains=keywords)
  
  # if'category' in request.GET:
  #   category_id = request.GET['category']
  #   if category_id:
  #     queryset_list = queryset_list.filter(category_id=category_id)

  # query_data = request.GET.copy()
  # if query_data.get('category'):
  #   try:
  #     query_data['category'] = int(query_data['category'])
  #   except ValueError:
  #     pass
    
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
  
  # categories = Category.objects.all()

  # context = {
  #   'products': queryset_list,
  #   'categories':categories,
  #   'values' : query_data
  # }

  # return render(request,'products/search.html',context)

def search(request):
  query_list = Product.objects.all()

  query = request.GET.get('q') or request.GET.get('keywords')
  category_id = request.GET.get('category')

  if query:
    query_list = query_list.filter(title__icontains=query)
  
  if category_id:
    query_list = query_list.filter(category_id=category_id)

  context={
    'products':query_list,
    'values':request.GET,
  }

  return render(request,'products/search.html',context)