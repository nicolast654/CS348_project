# Sales Reporting System – CS348 Project

**Author**: Nicolas Tabet\
**Course**: CS348 – Information Systems, Purdue University

## 📦 Overview

This is a simple sales reporting system built using **Flask**, **SQLite**, and **SQLAlchemy (ORM)**. The application allows a store manager to track products, sales, and generate reports efficiently. It demonstrates best practices in indexing, prepared statements, transaction management, and basic database optimization.

---

## 1. 📁 Indexes and Their Purpose

### 🔍 Index: `idx_product_category_id`

- **Table**: `product`
- **Column**: `category_id`
- **Purpose**: Optimizes queries filtering by product category.
- **Supported Queries**:
  ```sql
  SELECT * FROM product WHERE category_id = ?;
  ```
- **Usage**: Supports category filters in the sales report.

### 🔍 Index: `idx_sale_date`

- **Table**: `sale`
- **Column**: `date`
- **Purpose**: Speeds up filtering sales by date.
- **Supported Queries**:
  ```sql
  SELECT * FROM sale WHERE date = ?;
  ```
- **Usage**: Filters sales by date in the sales report.

### 🔍 Index: `idx_sale_product_id`

- **Table**: `sale`
- **Column**: `product_id`
- **Purpose**: Optimizes joins between `sale` and `product`.
- **Supported Queries**:
  ```sql
  SELECT * FROM product JOIN sale ON product.id = sale.product_id;
  ```
- **Usage**: Used in generating reports and updating stock levels.

---

## 2. 🛠️ Database Access Methods

As per projects requirements, I use both **prepared statements** and **ORM (SQLAlchemy)** for accessing the database. More implementation details are explained in the video.

---

## 3. 🔄 Transactions and Concurrent Access

Since this application is only designed for one user (the store manager), it doesn't expect concurrent access. However, by default, SQLite uses **SERIALIZABLE** transactions which ensure atomicity and consistency.

Example transaction:

```python
product.stock_level -= quantity
new_sale = Sale(product_id=id, quantity=quantity, date=sale_date)
db.session.add(new_sale)
db.session.commit()
```

SQLite’s SERIALIZABLE isolation level provides the highest consistency level, which is sufficient for a single-user application like this.

---

## 4. 🚀 How to Run the Application

To run the app:

1. Clone the repository:

   ```bash
   git clone https://github.com/nicolast654/CS348_project.git ~/cs348_project
   cd ~/cs348_project
   ```

2. Install the required Python modules:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python3 main.py
   ```

---

This project was completed as part of CS348 coursework at Purdue University. It is intended for educational use only.


