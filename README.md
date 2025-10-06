#  Flask Inventory Management System

This is a simple **Inventory Management Web Application** built with Flask.  
It helps users **manage products, track stock, move items between locations, and generate reports**.  
The app also has **Sign Up, Login, and Logout** functionality for security.  

---

##  How to Use

### 1️⃣ Sign Up (First-Time User)
- Open the app in your browser: `http://127.0.0.1:5000/`
- Click **Sign Up** in the top-right corner.
- Enter a **username** and **password**.
- After signing up, you will be automatically logged in.

### 2️⃣ Login (Returning User)
- Open the app again later.
- Click **Login** in the top-right corner.
- Enter your **username and password** to access the system.

### 3️⃣ Manage Products
- Go to the **Products** page.
- Add new products with **Product ID, Name, and Description**.
- Edit or delete existing products anytime.

### 4️⃣ Add Stock
- Go to **Add Stock**.
- Select a product, type the location, and enter the quantity.
- This increases stock at that location.

### 5️⃣ Move Stock
- Go to **Movements**.
- Select a product, enter **From Location** and **To Location**, and quantity.
- This moves stock from one location to another.

### 6️⃣ View Reports
- Go to **Report**.
- See:
  - Stock balance at each location
  - Total stock for each product
  - Movement history with **timestamps**

### 7️⃣ Logout
- When finished, click **Logout** from the top-right menu.

---
