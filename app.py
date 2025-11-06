from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load product data
def load_products():
    with open('data/products.json', 'r') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/product/<product_id>')
def product_details(product_id):
    products_data = load_products()
    product = None
    
    # Find the product by ID in the new structure
    for category in products_data['categories']:
        for p in category['products']:
            if p['id'] == product_id:
                product = p
                break
        if product:
            break
    
    return render_template('product-details.html', product=product)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/order-success')
def order_success():
    return render_template('order-success.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/api/products')
def api_products():
    products_data = load_products()
    return jsonify(products_data)

@app.route('/api/products/<category>')
def api_products_by_category(category):
    products_data = load_products()
    
    # Find the category in the categories array
    category_data = None
    for cat in products_data['categories']:
        if cat['id'] == category:
            category_data = cat
            break
    
    if category_data:
        return jsonify(category_data)
    else:
        return jsonify({'error': 'Category not found'}), 404

@app.route('/api/product/<product_id>')
def api_product(product_id):
    products_data = load_products()
    
    # Find the product by ID in the new structure
    for category in products_data['categories']:
        for product in category['products']:
            if product['id'] == product_id:
                return jsonify(product)
    
    return jsonify({'error': 'Product not found'}), 404

# New endpoint to get all categories
@app.route('/api/categories')
def api_categories():
    products_data = load_products()
    return jsonify(products_data['categories'])

# New endpoint to get featured products
@app.route('/api/products/featured')
def api_featured_products():
    products_data = load_products()
    featured_products = []
    
    for category in products_data['categories']:
        for product in category['products']:
            if product.get('featured', False):
                featured_products.append(product)
    
    return jsonify(featured_products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)