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

@app.route('/product/<int:product_id>')
def product_details(product_id):
    products = load_products()
    product = None
    
    # Find the product by ID
    for category in products.values():
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
    products = load_products()
    return jsonify(products)

@app.route('/api/products/<category>')
def api_products_by_category(category):
    products = load_products()
    return jsonify(products.get(category, {}))

@app.route('/api/product/<int:product_id>')
def api_product(product_id):
    products = load_products()
    
    for category in products.values():
        for product in category['products']:
            if product['id'] == product_id:
                return jsonify(product)
    
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)