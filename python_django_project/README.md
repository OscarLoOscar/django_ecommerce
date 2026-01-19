### Only_K E-commerce Platform (2026 Version)

Only_K is a sophisticated, semi-automated e-commerce solution built with Django 6.0. It is designed for boutique handmade jewelry businesses, featuring a robust product management system, session-based shopping carts, and an automated email notification system triggered by order status changes.

#### 🚀 Technical Stack

- Backend: Python 3.12+ / Django 6.0

- Database: PostgreSQL (Production-ready)

- Image Processing: Pillow (Automated resizing & aspect ratio maintenance)

- Authentication: Django-allauth (Google OAuth2 Integration)

- Environment: Python-dotenv for secure credential management

- Frontend: Bootstrap 4, FontAwesome, Custom JavaScript

---

#### 🛠️ Core Features

**1. Smart Product Management**

- Automated Image Optimization: Custom save() method using Pillow to resize all product images to a maximum of 500x500px while maintaining the aspect ratio.

- Category-Driven Logic: Automatic ring size defaults (Size 11 for rings, 0 for chains) based on category type selection.

**2. Advanced Order & Notification System**

- Status-Driven Signals: Uses Django Signals to monitor Order status changes.

- Automated Gmail SMTP: Automatically sends branded emails to customers when an order is marked as Paid, Shipping, or Shipped.

- Tracking Integration: Supports SF Express tracking numbers and manual payment receipt (bank transfer) verification.

**3. User Experience**

- Hybrid Shopping Cart: Supports both authenticated users and anonymous sessions.

- Multi-Auth: Custom backend allowing users to sign in via either Username or Email.

- Responsive UI: Dynamic "Read More" descriptions and categorized navigation.

---

#### 📊 Documentation & Architecture

The following diagrams represent the internal logic and architecture of the system:

**1. Entity Relationship Diagram (ERD)**

- **What it represents**: The "Skeleton" of the database. It defines how Users, Orders, and Products interact.

- **Key Logic**: Shows the `through` table relationships for `CartItems` and `OrderItems`, ensuring that product data (like price at the time of purchase) is preserved even if the original product is updated.

**2. System Mind Map**

- **What it represents**: The "Functional Scope." It categorizes the project into four pillars: Data Layer, Logic Layer, User Journey, and Tech Stack.

- **Key Logic**: It highlights the automation of Pillow and the Signal-based email system as core technical advantages.

**3. User Authentication Flow**

- **What it represents**: The "Security Logic." It maps out the path for both local registration and Google OAuth2 via `django-allauth`.

- **Key Logic**: Defines the redirect patterns and the fallback to custom `EmailOrUsernameModelBackend`.

**4. Order State Diagram**

- **What it represents**: The "Life Cycle" of a transaction.

- **Key Logic**: Visualizes the transition from `Pending` → `Paid` → `Shipping` → `Shipped`, mapping each state to a specific Email Signal trigger.

**5. Sequence Diagram**

- **What it represents**: The "Communication Flow." It shows the real-time interaction between the User's Browser, the Django Server, and the SMTP Email Server.

- **Key Logic**: Clearly identifies the `post_save` trigger point where the backend decides to fire an email based on database updates.

---

#### 🔧 Installation & Setup

1. **Clone the repository**:

```Bash
git clone <your-repo-url>
```

2. **Install Dependencies**:

```Bash
pip install -r requirements.txt
```

3. **Environment Variables**: Create a `.env` file in the root directory:

```bash
DEBUG=True
SECRET_KEY=your_secret_key
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
EMAIL_USER=your_gmail@gmail.com
EMAIL_PASS=your_app_password
```

4. **Database Migration**:

```Bash
python manage.py migrate
```

5. Run Server:

```Bash
python manage.py runserver
```
