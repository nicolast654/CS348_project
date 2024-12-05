from flask import Flask, request, render_template, redirect, url_for
from models import db, Product, Category, Sale
from datetime import datetime
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def populate_categories():
    with app.app_context():
        if not Category.query.first():
            db.session.add_all([
                Category(name="Electronics"),
                Category(name="Clothing"),
                Category(name="Groceries"),
                Category(name="Furniture"),
                Category(name="Toys")
            ])
            db.session.commit()

@app.route('/', methods = ['GET'])
def main():
    products = Product.query.all()
    categories = {category.id: category.name for category in Category.query.all()}
    return render_template('products.html', products = products, categories = categories)

@app.route('/add_products', methods = ['POST'])
def add_products():
	name = request.form["name"]
	category_id = int(request.form["category"])
	price = request.form["price"]
	stock = request.form["stock_level"]

	new_product = Product(name = name, category_id = category_id, price = price, stock_level = stock)
	db.session.add(new_product)
	db.session.commit()
	return redirect(url_for("main"))
    

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
	product = Product.query.get_or_404(id)
	if request.method == 'POST':
		product.name = request.form["name"]
		product.category_id = int(request.form["category"])
		product.price = request.form["price"]
		product.stock_level = request.form["stock_level"]
		db.session.commit()
		return redirect(url_for("main"))

	#categories = {category.id: category.name for category in Category.query.all()}
	return render_template('edit_product.html', product = product, categories = Category.query.all())

@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
	product = Product.query.get_or_404(id)
	db.session.delete(product)
	db.session.commit()
	return redirect(url_for("main"))

@app.route('/log_sale/<int:id>', methods=['GET', 'POST'])
def log_sale(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        date_str = request.form['date']

        sale_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        if quantity > product.stock_level:
            return f"Not enough stock for {product.name}. Available: {product.stock_level}", 400

        product.stock_level -= quantity
        new_sale = Sale(product_id=id, quantity=quantity, date=sale_date)
        db.session.add(new_sale)
        db.session.commit()

        return redirect(url_for('main'))

    return render_template('log_sale.html', product=product)

@app.route('/sales_report', methods=['GET', 'POST'])
def sales_report():
    categories = Category.query.all()
    results = []
    stats = {}

    if request.method == 'POST':
        category_id = request.form.get('category')
        category_id = int(category_id) if category_id else None

        sale_date = request.form.get('sale_date')
        sale_date = datetime.strptime(sale_date, '%Y-%m-%d').date() if sale_date else None

        results = generate_sales_report(category_id, sale_date)

        stats = {
            "total_revenue": sum(row.total_revenue for row in results),
            "total_quantity": sum(row.total_quantity for row in results),
            "top_selling_product": results[0].product_name if results else "None",
        }

    return render_template('sales_report.html', categories=categories, results=results, stats=stats)

def generate_sales_report(category_id=None, sale_date=None):
    base_query = """
        SELECT 
            p.name AS product_name,
            s.date AS sale_date,
            SUM(s.quantity) AS total_quantity,
            SUM(s.quantity * p.price) AS total_revenue
        FROM 
            product p
        JOIN 
            sale s ON p.id = s.product_id
        WHERE 
            1=1
            {category_filter}
            {date_filter}
        GROUP BY 
            p.id, s.date
        ORDER BY 
            total_quantity DESC
    """

    category_filter = " AND p.category_id = :category_id" if category_id else ""
    date_filter = " AND s.date = :sale_date" if sale_date else ""

    final_query = base_query.format(
        category_filter=category_filter,
        date_filter=date_filter
    )

    params = {}
    if category_id:
        params['category_id'] = category_id
    if sale_date:
        params['sale_date'] = sale_date

    result = db.session.execute(text(final_query), params)

    rows = result.fetchall()

    return rows


if __name__ == "__main__":
	with app.app_context():
		db.create_all()
		populate_categories()
	app.run(port=8000, debug=True)
