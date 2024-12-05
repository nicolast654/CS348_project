from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import Index

db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_level = db.Column(db.Integer, default=0)

    __table_args__ = (
        Index('idx_product_category_id', 'category_id'),
    )

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    __table_args__ = (
        Index('idx_sale_date', 'date'),
        Index('idx_sale_product_id', 'product_id'),
    )
