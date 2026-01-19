# python_project

記住用家最後睇過嘅產品 ID

```Python
def product_detail(request, pk):
    # 儲存 ID 到 Session
    request.session['last_viewed_product'] = pk

    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def show_recommendation(request):
    # 喺另一個 View 攞返出嚟
    last_pk = request.session.get('last_viewed_product')
    # ... 根據呢個 ID 搵相關產品 ...
```

---

\_search_form.html

```html
<option
  value="{{category.id}}"
  {%
  if
  category.id|slugify=""
  ="values.category"
  %}
  selected
  {%
  endif%}
>
  {{category.title}}
</option>
```

---

---

notes @12/01/2026
https://icons.getbootstrap.com/icons/threads/

Looking for logo:

```bash
https://fontawesome.com/
```

方案 B：重置遷移（最推薦，確保資料庫與代碼同步）
刪除出問題的遷移文件： 刪除 orders/migrations/ 資料夾內除了 **init**.py 以外的所有新生成的 000x\_... 檔案（特別是 0006）。

偽裝回退（Fake rollback）： 告訴 Django 我們先當作這些改動還沒發生：

```Bash
python manage.py migrate --fake orders zero
```

(注意：這會清空該 app 的遷移紀錄，但不會刪除表格資料)

重新生成遷移：

```Bash
python manage.py makemigrations orders
```

強制對齊（Fake apply）： 如果資料庫已經手動改過欄位，執行：

```Bash
python manage.py migrate --fake-initial orders
```

或者嘗試正常 migrate：

```Bash
python manage.py migrate orders
```

---

```
ALTER TABLE orders_order ADD COLUMN is_paid_sent boolean DEFAULT FALSE;
ALTER TABLE orders_order ADD COLUMN is_shipping_sent boolean DEFAULT FALSE;
ALTER TABLE orders_order ADD COLUMN is_shipped_sent boolean DEFAULT FALSE;
ALTER TABLE orders_order ADD COLUMN tracking_number varchar(100);
```

---

```bash
pip install django-allauth requests PyJWT
```

settings.py:

```python
INSTALLED_APPS = [
    ...
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', # Google 提供商
    ...
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/' # 登入後去邊
SOCIALACCOUNT_LOGIN_ON_GET = True # 撳掣即跳轉，唔使再確認一次
```

```
喺 Admin 後台登記 Google Client ID
雖然你有 JSON，但 Django 需要喺資料庫紀錄呢組 ID：

執行 python manage.py migrate（建立 allauth 相關 Table）。

入 Django Admin -> Social Applications -> Add Social Application。

Provider: 選 Google。

Name: 求其改（例如 "Google Login"）。

Client id: 填入你 JSON 入面嗰串長 ID。

Secret key: 填入你 JSON 入面嗰串密鑰。

Chosen sites: 將右邊嘅 example.com（或 localhost）搬去左邊。
```
