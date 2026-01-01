1. Show all product , 有貨同 sold out 都要 show
2. 加入購物車，入左購物車會有個 window 彈出，然後顯示所有 shopping cart product 同價錢
3. show product 既 description
4. 送貨及付款方式
   1. 送貨方式：
      1. 下次 booth 自取
      2. 順豐到付
   2. 付款方式：
      - 信用卡付款
      - Payme
      - 支付寶 (HK)\_SHOPLINE Payments
      - Apple Pay
      - 微信支付

- 3.同 4.要做到 Accordion（手風琴）或者 Collapsible（可摺疊組件）->
  - click 一個按鈕(顯示＋號)，會展開商品描述，再按同一個按鈕（顯示減號），會收埋商品描述

5. top bar 有公司 logo， 右手面有：
   1. search product
   2. login/Register
   3. shopping cart
6. Navigation bar 要有
   1. 月份限定
   2. 玻璃球系列
   3. 韓國飾物
   4. 韓國代
   5. Workshop 日期
   6. Pick up & Delivery
   7. 條款及細則

---

```python
from django.db import models
from django.contrib.auth.models import User
```
