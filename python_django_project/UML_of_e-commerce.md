```mermaid
mindmap
  root((Only_K Ecommerce V2))
    Home_Page["Home Page <br/>(Mainpage / Index)"]
        Showcase["Showcase (Bootstrap Carousel)"]
            Custom_Arrows["pink color: #ffb7b7ff"]
            IG_Video["Instagram 影片嵌入 (Embed)"]
        Product_Listing["產品列表 (product_list)"]
            Filter_Logic["動態分類篩選 <br/>(?category_type=)"]
            Search_Q["搜尋功能 <br/>(Q Object: 標題/描述)"]
            Paginator["分頁功能 (每頁 3 件)"]
        Cart_Logic["購物車系統 (Carts/CartItems)"]
            Session_Support["Session (未登錄購物)"]
            Context_Processor["購物車數量"]

    Product_Detail["Product Detail (產品詳情)"]
        Image_System["多圖System (image_00 - 04)"]
            Pillow_Resize["自動壓縮 (500x500 <br/>thumbnail)"]
        Smart_Size["Intelligence尺寸 (Save Logic)"]
            Ring_Size["戒指: 預設 11"]
            Chain_Size["鏈類: 自動歸 0"]
        Status_Info["商品資訊"]
            Stock_Count["Run Time Database"]
            Policy_Info["送貨and條款"]

    Checkout_Order["Order System (訂單與結帳)"]
        Delivery_Methods["送貨 (DELIVERY_CHOICES)"]
            Booth["下次 Booth 自取"]
            SF_Express["順豐到付 (SF Region/Address)"]
        Payment_Gateways["支付 (PAYMENT_CHOICES)"]
            Local_Pay["Payme / 支付寶HK / 八達通"]
            Credit_Mobile["信用卡 / Apple Pay"]
        Proof_Upload[" payment_receipt Upload"]
            Timestamp["Upload time record"]

    Backend_Automation["Backend Automation"]
        Signals["Django Signals (post_save)"]
            Status_Monitor["狀態監控: <br/>Shipping/Shipped"]
            Email_System["Gmail SMTP 自動通知"]
                Template_A["付款確認信 (is_paid_sent)"]
                Template_B["包裝中通知 (is_shipping_sent)"]
                Template_C["出貨通知 + 順豐單號 (is_shipped_sent)"]
        Admin_Management["Admin 管理"]
            Status_Control["手動切換狀態觸發 Signal"]
            Security["Environment Variables (.env 管理)"]

    User_Section["User Section (Member)"]
        Auth["身份驗證"]
            Standard["Login / Register / Logout"]
            Social["Google Login"]
        Dashboard["會員中心"]
            Order_History["歷史Order追蹤"]

    Footer_Info["Footer"]
        Contact["聯絡 (WhatsApp / IG)"]
        Legal["Legal Pages (Pages App)"]
            Terms["條款及細則 (T&C)"]
            Privacy["私隱政策"]
```

---

### User Authentication Flow :

```mermaid
graph TD
  V((Visitor)) --- UI_Header["Header / Registration Page"]

  subgraph Allauth_Google [Google OAuth 流程 - django-allauth]
      direction LR
      UI_Header ---- UC02("Google Login 按鈕")
      UC02 -->|URL: /accounts/google/login/| UC03("Google OAuth 驗證")
      UC03 -.->|Success| UC04("建立 SocialAccount 關聯")
      UC04 -->|Redirect| UC_RED("/")
  end

  subgraph Local_Auth [本地帳號流程 - users App]
      direction TB
      UI_Header --- UC05("Username/Email 登入")
      UC05 -->|Backend| UC_Backend("EmailOrUsernameModelBackend")

      UI_Header --- UC06("用戶註冊 (Register)")
      UC06 -->|Validation| UC12("檢查重複 & 密碼強度")

      UC_Backend -.->|Login Success| UC14("Dashboard / Home")
      UC12 -.->|Success| UC14
  end

  subgraph Session_Mgmt [會話管理]
      UC14 --- UC15("Session Persistence")
      UC15 --- REM["Remember Me (待實作)"]
      UC14 --> LOGOUT["Logout (users:logout)"]
  end

  subgraph Password_Security [安全與找回]
      UC05 --- UC08("Forget Password (待實作)")
      UC08 -.->|需配置| UC09("Django Auth Views / SMTP")
  end

  UC14 -->|Context| CP["Cart Context Processor (顯示購物車數量)"]
```

---

### 結帳流程 與 帳戶管理 :

```mermaid
graph TD
    M((Member)) --- UC_VC(View <br/>/ Update Shopping Cart)
    M --------- UC_MA(Manage <br/>Account)

    subgraph Shopping_Cart [購物車邏輯 - carts App]
    UC_VC --> UC19("有庫存")
    UC_VC --> UC20("Sold Out / 下架") --> UC_VC
    UC19 --> UC_CO("Check Out / 前往結帳")
    end

    subgraph Checkout_Process [結帳與訂單流 - orders App]
    UC_CO --- UC15("提交訂單 (Place Order)")
    UC15 --- UC14("選擇支付: Payme/Alipay/Octopus...")
    UC14 --> UC13("選擇送貨: 自取/順豐到付")
    UC13 --> UC_UPLOAD("上傳付款憑證 (payment_receipt)")

    UC_UPLOAD -- "Admin 核實後改為 Paid" --> UC_SIGNAL("觸發 Signal: 發送確認 Email")
    UC_SIGNAL --> UC_STATUS("狀態演變: Paid > Shipping<br> > Shipped")
    end

    subgraph Account_Management [帳戶管理 - users App]
    UC_MA ----- UC11("查看歷史訂單 (Dashboard)")
    UC_MA --- UC12("修改個人資料")
    UC_MA ---- UC_VPW("忘記密碼 (待實作)")
    UC11 --> UC_TRACK("查詢物流單號 (tracking_number)")
    end

    M --> UC21("Member Popup Menu")
    subgraph Member_Popup_menu [會員快捷選單]
    UC21 ----> UC22("View Payment Record")
    UC21 --> UC_23("Logout (登出)")
    UC21 -----> UC24("Change Member Info")
    UC24 -.-> UC25("Success Msg")
    UC_23 -.-> UC26("Success Msg")
    end

    style M fill:#bbf,stroke:#333,stroke-width:2px
    style UC_SIGNAL fill:#f96,stroke:#333,stroke-width:2px
    style UC_UPLOAD fill:#dfd,stroke:#333,stroke-width:2px
```

---

### Admin（管理員）流程圖:

```mermaid
graph LR
    A((Admin)) --- UC13("產品管理 (CRUD)")
    subgraph Product_Detail [產品自動化細節]
        UC13 --- UC13_1("圖片自動縮放 (Pillow 500px)")
        UC13 --- UC13_2("智能尺寸校正 (save logic)")
        UC13 --- UC13_3("上架/下架控制 (is_published)")
    end

    A --- UC15("分類管理 (Navbar)")
    UC15 --- UC15_1("排序控制 (order 欄位)")

    A --- UC16("訂單與物流處理")
    subgraph Order_Workflow [訂單核心邏輯]
        UC16 --- UC16_1("審核入數紙 (payment_receipt)")
        UC16 --- UC16_2("填寫物流單號 (tracking_number)")
        UC16 --- UC16_3("變更狀態 (Paid/Shipping/Shipped)")
        UC16_3 -.->|自動觸發| UC_MAIL("Gmail SMTP 通知用戶")
    end

    A --- UC17("用戶管理 (User)")
    A --- UC18("內容維護 (Pages App)")
    UC18 --- UC18_1("更新條款/私隱政策")

    A --- UC_RPT("數據分析 (Admin Dashboard)")

    style A fill:#bfb,stroke:#333,stroke-width:2px
    style UC_MAIL fill:#f96,stroke:#333,stroke-width:2px
```

---

### FrontEnd User Flow

```mermaid
graph TD
    V((訪客)) --> PL["產品列表 (product_list.html)"]

    subgraph PL_Interaction [列表頁交互]
        PL --> CAT["分類導航 (耳環/戒指/手鏈...)"]
        PL --> SEARCH["關鍵字搜尋 (Q Object)"]
        PL --> READ_MORE["JS Toggle: Read More/Close"]
        PL --> PAGI["分頁切換 <br/>(?page=)"]
    end

    PL --> PD["產品詳情 (product_detail.html)"]
    PD --> ADD["加入購物車 (AJAX)"]

    subgraph Cart_Interaction [購物車交互 - cart_detail.html]
        ADD --> CV["查看購物車"]
        CV --> QTY["數量增減 (+/- Button)"]
        CV --> RMV["移除項目 (Trash Icon)"]
        CV --> TOTAL["Subtotal 自動計算 (get_subtotal)"]
    end

    TOTAL --> CHECKOUT["訂單結帳 (orders:checkout)"]
```

---

## Add item in Shopping Cart (sequenceDiagram):

```mermaid
sequenceDiagram
    autonumber
    actor U as User (Browser)
    participant B as Backend (Django)
    participant DB as Database (PostgreSQL)
    participant E as Email Service (Gmail SMTP)

    Note over U, B: 購物車與 Session 操作
    U->>B: 新增產品入購物車 (AJAX /api/add/)
    B->>DB: 建立 CartItem (連動 Session/User)
    B-->>U: 更新 Navbar 購物車數量 (Context Processor)

    Note over U, B: 結帳流程 (Checkout)
    U->>B: 點擊「前往結帳」
    B->>DB: 建立 Order (Status: Pending)
    U->>B: 上傳入數紙 (payment_receipt)
    B->>DB: 儲存圖片並記錄上傳時間

    Note over B, E: Admin 核實與自動通知 (Signals)
    rect rgb(240, 240, 240)
        Note right of B: Admin 在後台手動更改 Status 為 'Paid'
        B->>DB: 更新 Order 狀態
        B->>B: 觸發 signals.py (post_save)
        B->>E: 執行 send_mail()
    end

    E-->>U: 用戶收到「付款確認」Email

    Note over B, E: 物流階段
    rect rgb(240, 240, 240)
        Note right of B: Admin 填寫 tracking_number 並改為 'Shipped'
        B->>B: 再次觸發 Signal
        B->>E: 寄出「已出貨」Email (含順豐單號)
    end
    E-->>U: 用戶收到「出貨通知」Email
```

---

### Order State Diagram :

```mermaid
stateDiagram-v2
    [*] --> InCart: 加入產品 (Session/User Cart)

    state InCart {
        [*] --> Adjusting: 修改數量/移除
        Adjusting --> [*]: 購物車清空
    }

    InCart --> OrderCreated: 點擊 Checkout (建立 Order)

    state OrderCreated {
        [*] --> Pending: 狀態預設為 Pending
        Pending --> AwaitingVerification: 用戶上傳入數紙 (payment_receipt)
    }

    AwaitingVerification --> Paid: Admin 手動核實付款

    state Paid {
        [*] --> Email_Paid: 觸發 Signal (is_paid_sent)
        Email_Paid --> Preparing: 賣家準備貨物
    }

    Preparing --> Shipping: Admin 改為 Shipping

    state Shipping {
        [*] --> Email_Shipping: 觸發 Signal (is_shipping_sent)
        Email_Shipping --> Carrier: 交給快遞公司 (SF Express)
    }

    Carrier --> Shipped: Admin 填寫 tracking_number 並改狀態

    state Shipped {
        [*] --> Email_Shipped: 觸發 Signal (is_shipped_sent)
        Email_Shipped --> Delivered: 用戶收到貨品
    }

    Delivered --> [*]: 交易完成
```

---

```mermaid
erDiagram
    %% 會員與帳戶系統
    USER ||--o{ ORDER : "places"
    USER ||--o{ PURCHASE_HISTORY : "has"
    USER ||--o| CART : "owns"

    %% 產品與分類
    CATEGORY ||--o{ PRODUCT : "classifies"

    %% 購物車邏輯 (Through Table)
    CART ||--o{ CART_ITEM : "contains"
    PRODUCT ||--o{ CART_ITEM : "added_to"

    %% 訂單邏輯 (Through Table)
    ORDER ||--o{ ORDER_ITEM : "includes"
    PRODUCT ||--o{ ORDER_ITEM : "ordered_as"

    USER {
        int id PK
        string username
        string email
        string password
        string phone
        datetime last_login
    }

    PRODUCT {
        int id PK
        int category_id FK
        string title
        decimal price
        int stock_count
        int size
        image image_00
        boolean is_published
    }

    CATEGORY {
        int id PK
        string name
        string category_type
        int order
    }

    CART {
        int id PK
        int user_id FK
        string session_id
        datetime created_at
    }

    CART_ITEM {
        int id PK
        int cart_id FK
        int product_id FK
        string size
        int quantity
    }

    ORDER {
        int id PK
        int user_id FK
        decimal total_price
        string status
        string delivery_method
        string tracking_number
        image payment_receipt
        boolean is_paid_sent
    }

    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        decimal price
        int quantity
        string size
    }

    PURCHASE_HISTORY {
        int id PK
        int user_id FK
        int product_id FK
        datetime created_at
    }
```
