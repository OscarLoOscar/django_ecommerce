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
    <option value="{{category.id}}" {% if category.id|slugify== values.category %} selected {% endif%}>
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
