# django_ecommerce

整埋 HTML 版嘅 Email（即係有粗體、有色、甚至有圖嗰種）

將 register 改成「JSON 格式」嘅 Response（即係唔再 redirect，而係 return 一個狀態碼），等 React 第時可以直接接收？

寫埋 React 銜接最需要的 JsonResponse 版本嗎？（即係唔再用 render 網頁，而係回傳 { "status": "success", "order_id": 123 } 這種格式

---

users/views.py

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt # 喺開發 React 測試時常用，正式版建議用 Token
def api_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return JsonResponse({"status": "success", "message": "Logged in", "user": user.username})
        return JsonResponse({"status": "error", "message": "Invalid credentials"}, status=401)

@login_required
def api_user_profile(request):
    """呢個就是你之前想做嘅 Dashboard 資料來源"""
    user = request.user
    # 攞返購買歷史
    history = PurchaseHistory.objects.filter(user=user)
    history_data = [{"product": h.product.title, "date": h.purchased_at} for h in history]

    return JsonResponse({
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "purchase_history": history_data
    })
```

carts/views.py

```python
# carts/views.py
@login_required
def api_get_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    cart_data = []
    for item in items:
        cart_data.append({
            "id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.title,
            "price": str(item.product.price),
            "quantity": item.quantity,
            "image": item.product.image.url if item.product.image else ""
        })

    return JsonResponse({"items": cart_data, "total": sum(float(i['price']) * i['quantity'] for i in cart_data)})
```

```bash
my_project/
├── users/          <-- 處理登入、註冊、Profile、PurchaseHistory
├── products/       <-- 產品列表、搜尋、詳情
├── categories/     <-- 分類清單
├── carts/          <-- 購物車邏輯
├── cartitems/      <-- 購物車細項
├── orders/         <-- 結賬、Order、Email Signals
├── orderitems/     <-- 訂單細項
└── manage.py
```

---

```bash
CORS：因為 React (Port 3000) 同 Django (Port 8000) 唔同 Port，你需要裝 django-cors-headers。
```

---

```bash
真實 Project 仲差咩功能？ (功能補全)
作為一個真實嘅 E-commerce，你目前只有「睇產品」同「結賬」，仲差以下呢幾舊大嘢：

購物車管理 (Cart Management)：加嘢入車、減數量、刪除項目。

產品搜尋與進階篩選 (Search & Filter)：按名字搵嘢。

用戶中心數據 (User Dashboard Data)：React 需要攞到當前用家的訂單紀錄。

支付狀態更新 (Payment Trigger)：你的 Signal 寫咗 status=="Paid" 先寄信，但目前冇地方會將 Order 轉做 Paid。
```

---

```
五、 最後的專業建議
CORS Setup: React 同 Django 唔同 Port，你一定要裝 django-cors-headers 並且喺 settings.py 嘅 MIDDLEWARE 最頂加埋佢，否則 React fetch 唔到嘢。

CSRF: React 傳 POST 畀 Django 會遇到 CSRF 問題。開發時可以喺 View 加 @csrf_exempt，但正式環境建議用 JWT (JSON Web Token)。

Image URL: 確保 settings.py 有設定 MEDIA_URL 同 MEDIA_ROOT，React 先可以透過網址睇到產品圖。
```
