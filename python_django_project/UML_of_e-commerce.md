```mermaid
mindmap
  root((Ecommerce Website))
    Home_Page["Home Page (主頁)"]
        Product_Grid["產品網格 (Show All Products)"]
            Status_Tag["標籤: 有貨 / Sold Out"]
            Action["加入購物車按鈕"]
        Cart_Modal["Shopping Cart Window (彈出式)"]
            List["顯示所有已選產品及單價"]
            Calculations["總計金額 (Total Price)"]
            Checkout_Btn["前往結帳按鈕"]
    Header["Header (頂部欄)"]
        Top_Bar["Top Bar (公司 Logo)"]
            Search["Search Product (搜尋)"]
            Auth["Login / Register (登入註冊)"]
            Cart_Icon["Shopping Cart (小圖示)"]
        Navigation_Bar["Navigation Bar (導航)"]
            Cat1["月份限定"]
            Cat2["玻璃球系列"]
            Cat3["韓國飾物 / 代購"]
            Cat4["Workshop 日期"]
            Cat5["Pick up & Delivery"]
            Cat6["條款及細則"]
    Sub_Page["Sub Page (產品詳情頁)"]
        Gallery["產品圖片輪播"]
        Collapsible_Section["可摺疊組件 (Accordion)"]
            Desc["商品描述 (+/- 按鈕切換)"]
            Policy["送貨及付款詳情 (+/- 按鈕切換)"]
        Delivery_Methods["送貨方式"]
            Self_Pick["下次 Booth 自取"]
            SF_Express["順豐到付"]
        Payment_Gateways["付款方式"]
            Credit_Card["信用卡"]
            Local_Pay["Payme / 支付寶HK / 微信支付"]
            Mobile_Pay["Apple Pay"]
    Side_Bar["Side Bar (側邊欄 / 常用功能)"]
        Filter["進階篩選 (價錢/顏色)"]
        Quick_Links["快速連結 (常見問題)"]
        User_Menu["會員專區 (訂單查詢)"]
    Footer["Footer (底部)"]
        Contact["聯絡資訊 (Whatsapp/IG)"]
        Copyright["版權聲明"]
        T_C["服務條款簡述"]
```

---

---

```mermaid
graph TD
  V((Visitor)) --- UC01(Visitor popup menu)

  subgraph Login_Section [登入流程]
      direction LR
      UC01 ---- UC02("Login using Google ac")
      UC02 -.-> UC03("Google Login")
      UC02 -.-> UC04("Return msg from Google")

      UC01 --- UC05("Username login")
      UC07("Remember Me") --> UC05
      UC05 -.-> UC14("Login Success / Fail msg")
  end

  subgraph Password_Section [密碼管理]
      direction LR
      UC05 ----- UC08("Forget Password")
      UC08 -.-> UC09("Confirm Identity")
      UC08 --- UC10("Reset Password")
      UC10 -.-> UC11("Success Reset Password")
  end

  subgraph Register_Section [註冊流程]
      direction LR
      UC01 --------- UC06("Register")
      UC06 -.-> UC12("Verify New User Name")
      UC06 -.-> UC13("Register Success/Fail Message")
  end
```

---

```mermaid
graph TB
    M((Member)) --- UC_VC(View <br/>/ Update Shopping Cart)
    M --------- UC_MA(Manage <br/>Account)

    subgraph Checkout_Process [結帳流程]
    UC_CO --- UC15(Place Order <br/>/ 提交訂單)
    UC15 --- UC14("Payment: Payme<br/>/Alipay<br/>/ApplePay")
    UC14 --> UC13("選擇送貨: 自取/順豐")
    UC20 --> UC16("Delete Item") --> UC20
    UC13 --Include--> UC17("Change All <br/>Items to "Paid"")
    end
    UC17 --Include-->UC18("Make Transfer")

    subgraph Account_Management [帳戶管理]
    UC_MA ----- UC11(View <br/>Order History)
    UC_MA --- UC12(Update Profile <br/>/ 修改資料)
    UC_MA ---- UC_VPW(Verify <br/>/ Reset Password)
    end

    subgraph Shopping_Cart [Shopping Cart]
    UC_VC --> UC19("Have Stock")
    UC_VC --> UC20("Sold Out") --> UC_VC
    UC19 --> UC_CO("Check Out")
    end

    M --> UC21("Member <br/>Popup menu")
    subgraph Member_Popup_menu [Member Popup Menu]
    UC21 ----> UC22("View payment <br/>Record")
    UC21 --> UC_23("Logout")
    UC21 -----> UC24("Change <br/>Member Info")
    UC24 --Include-->UC25("Show <br/>Success Msg")
    UC_23 --Include-->UC26("Show <br/>Success Msg")
    end

    style M fill:#bbf,stroke:#333,stroke-width:2px
```

---

---

```mermaid
graph LR
    A((Admin)) --- UC13("產品管理 (CRUD, 上架/下架)")
    UC13 --- UC14("庫存管理 (更新 Stock Count)")
    A --- UC15("分類管理 (Navbar 項目維護)")
    UC13 --- UC16("訂單處理 (更改送貨狀態/確認付款)")
    A --- UC17("用戶管理 (查看/禁用會員)")
    A --- UC18("更新條款及細則")
    A --- UC_RPT(查看銷售報表與分析)

    style A fill:#bfb,stroke:#333,stroke-width:2px
```

---

## Add item in Shopping Cart :

```mermaid
sequenceDiagram
    autonumber
    actor M as Member (React)
    participant B as Backend (Django)
    participant DB as Database
    participant P as Payment Gateway (e.g. Payme/Stripe)
    participant E as Email Service

    Note over M, B: 購物車操作
    M->>B: 新增 2 樣產品入購物車
    B->>DB: 更新 CartItem (數量: 2)
    M->>B: 移除 (Cancel) 其中一件產品
    B->>DB: 更新 CartItem (數量: 1)

    Note over M, B: 結帳流程
    M->>B: 點擊「確認結帳」
    B->>DB: 檢查庫存 (Stock Check)
    B-->>M: 顯示訂單總計 (含送貨方式選擇)
    M->>B: 選擇送貨及付款方式 (Confirm Order)
    B->>DB: 建立訂單 (Status: Pending)

    Note over M, P: 付款與通知
    M->>P: 進行付款 (導向支付頁面)
    P-->>B: 付款成功回傳 (Webhook/Callback)
    B->>DB: 更新訂單狀態 (Status: Paid)
    B->>E: 觸發寄送通知郵件

    E-->>M: 收到確認 Email (訂單詳情)
```

---

```mermaid
stateDiagram-v2
    [*] --> InCart: 加入第 1 件產品

    state InCart {
        [*] --> Adjusting: 增加/減少數量
        Adjusting --> Adjusting: 修改 Item
        Adjusting --> [*]: 移除項目至清單為空
    }

    InCart --> Checkout: 點擊「確認結帳」

    state Checkout {
        [*] --> StockChecking: 系統檢查庫存
        StockChecking --> InfoEntry: 庫存足夠
        StockChecking --> InCart: 庫存不足
        InfoEntry --> OrderCreated: 確認送貨及付款
    }

    state OrderCreated {
        [*] --> PendingPayment
    }

    OrderCreated --> PendingPayment: 產生訂單 (Pending)

    state PendingPayment {
        [*] --> Redirecting: 導向支付頁面
        Redirecting --> Success: 付款成功
        Redirecting --> Failed: 付款失敗
    }

    Failed --> PendingPayment: 重新嘗試
    Success --> Paid: 更新訂單狀態 (Paid)

    state Paid {
        [*] --> Notification: 觸發 Email 邏輯
    }

    Notification --> [*]: 完成流程
```

---

---

```python
STATUS_CHOICES = (
    ('pending', 'Pending Payment'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('canceled', 'Canceled'),
)
status = models.CharField(choices=STATUS_CHOICES, default='pending')
```

---

```mermaid
erDiagram
    USER ||--|| CART : "one-to-one"
    USER ||--o{ ORDER : "places"
    CATEGORY ||--o{ PRODUCT : "contains"
    CART ||--|{ CART_ITEM : "has"
    PRODUCT ||--|{ CART_ITEM : "added_to"
    ORDER ||--|{ ORDER_ITEM : "includes"
    PRODUCT ||--o{ ORDER_ITEM : "purchased_as"

    USER {
        int id
        string username
        string email
    }
    CATEGORY {
        int id
        string name
        int order
    }
    PRODUCT {
        int id
        string title
        decimal price
        int stock_count
        text description
    }
    ORDER {
        int id
        string status
        string delivery_method
        string payment_method
        decimal total_price
    }
```
