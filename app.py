from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import os
import uuid
from werkzeug.utils import secure_filename

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///animecosplay.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-here')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    # Initialize extensions with app
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Create upload directory
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app

app = create_app()

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat(),
            'is_admin': self.is_admin
        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url
        }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255), nullable=False)
    additional_images = db.Column(db.JSON)
    sizes = db.Column(db.JSON, nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    stock_quantity = db.Column(db.Integer, default=0)
    featured = db.Column(db.Boolean, default=False)
    badge = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    category = db.relationship('Category', backref='products')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'original_price': self.original_price,
            'rating': self.rating,
            'review_count': self.review_count,
            'image_url': self.image_url,
            'additional_images': self.additional_images or [],
            'sizes': self.sizes or [],
            'in_stock': self.in_stock,
            'stock_quantity': self.stock_quantity,
            'featured': self.featured,
            'badge': self.badge,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'created_at': self.created_at.isoformat()
        }

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    size = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'size': self.size,
            'created_at': self.created_at.isoformat()
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), default='pending')
    shipping_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='orders')
    items = db.relationship('OrderItem', backref='order', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'shipping_address': self.shipping_address,
            'created_at': self.created_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(10))
    
    product = db.relationship('Product', backref='order_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product.name,
            'product_image': self.product.image_url,
            'quantity': self.quantity,
            'price': self.price,
            'size': self.size,
            'subtotal': self.quantity * self.price
        }

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='wishlist_items')
    product = db.relationship('Product', backref='wishlist_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': self.product.to_dict(),
            'created_at': self.created_at.isoformat()
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200))
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='reviews')
    product = db.relationship('Product', backref='reviews')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name,
            'product_id': self.product_id,
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'created_at': self.created_at.isoformat()
        }

# JWT configuration
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)

# Routes
@app.route('/')
def home():
    return jsonify({"message": "AnimeCosplay India API is running!"})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'AnimeCosplay API is running'})

# Auth Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({'message': 'Name, email and password are required'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'User already exists with this email'}), 400
        
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            address=data.get('address')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=user)
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'message': 'Error creating user', 'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user)
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user': user.to_dict()
            })
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
            
    except Exception as e:
        return jsonify({'message': 'Error during login', 'error': str(e)}), 500

# Product Routes
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        category_id = request.args.get('category_id')
        featured = request.args.get('featured')
        search = request.args.get('search')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        
        query = Product.query
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        if featured:
            query = query.filter_by(featured=True)
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))
        
        products = query.all()
        
        return jsonify({
            'products': [product.to_dict() for product in products],
            'total': len(products)
        })
        
    except Exception as e:
        return jsonify({'message': 'Error fetching products', 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({'product': product.to_dict()})
    except Exception as e:
        return jsonify({'message': 'Error fetching product', 'error': str(e)}), 500

# Category Routes
@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify({'categories': [category.to_dict() for category in categories]})
    except Exception as e:
        return jsonify({'message': 'Error fetching categories', 'error': str(e)}), 500

# Cart Routes
@app.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        current_user = get_jwt_identity()
        cart_items = Cart.query.filter_by(user_id=current_user).all()
        
        total = sum(item.quantity * item.product.price for item in cart_items)
        
        return jsonify({
            'cart_items': [item.to_dict() for item in cart_items],
            'total': total
        })
    except Exception as e:
        return jsonify({'message': 'Error fetching cart', 'error': str(e)}), 500

@app.route('/api/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        size = data.get('size', 'M')
        
        if not product_id:
            return jsonify({'message': 'Product ID is required'}), 400
        
        cart_item = Cart.query.filter_by(
            user_id=current_user, 
            product_id=product_id,
            size=size
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = Cart(
                user_id=current_user,
                product_id=product_id,
                quantity=quantity,
                size=size
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        return jsonify({'message': 'Item added to cart', 'cart_item': cart_item.to_dict()})
        
    except Exception as e:
        return jsonify({'message': 'Error adding to cart', 'error': str(e)}), 500

@app.route('/api/cart/<int:cart_item_id>', methods=['DELETE'])
@jwt_required()
def remove_cart_item(cart_item_id):
    try:
        current_user = get_jwt_identity()
        cart_item = Cart.query.filter_by(id=cart_item_id, user_id=current_user).first_or_404()
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({'message': 'Item removed from cart'})
        
    except Exception as e:
        return jsonify({'message': 'Error removing cart item', 'error': str(e)}), 500

# Wishlist Routes
@app.route('/api/wishlist', methods=['GET'])
@jwt_required()
def get_wishlist():
    try:
        current_user = get_jwt_identity()
        wishlist_items = Wishlist.query.filter_by(user_id=current_user).all()
        
        return jsonify({'wishlist': [item.to_dict() for item in wishlist_items]})
    except Exception as e:
        return jsonify({'message': 'Error fetching wishlist', 'error': str(e)}), 500

@app.route('/api/wishlist', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        product_id = data.get('product_id')
        
        if not product_id:
            return jsonify({'message': 'Product ID is required'}), 400
        
        existing_item = Wishlist.query.filter_by(user_id=current_user, product_id=product_id).first()
        if existing_item:
            return jsonify({'message': 'Item already in wishlist'}), 400
        
        wishlist_item = Wishlist(user_id=current_user, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        
        return jsonify({'message': 'Item added to wishlist', 'wishlist_item': wishlist_item.to_dict()})
        
    except Exception as e:
        return jsonify({'message': 'Error adding to wishlist', 'error': str(e)}), 500

@app.route('/api/wishlist/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(product_id):
    try:
        current_user = get_jwt_identity()
        wishlist_item = Wishlist.query.filter_by(user_id=current_user, product_id=product_id).first_or_404()
        
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({'message': 'Item removed from wishlist'})
        
    except Exception as e:
        return jsonify({'message': 'Error removing from wishlist', 'error': str(e)}), 500

# Order Routes
@app.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        cart_items = Cart.query.filter_by(user_id=current_user).all()
        
        if not cart_items:
            return jsonify({'message': 'Cart is empty'}), 400
        
        total_amount = sum(item.quantity * item.product.price for item in cart_items)
        
        # Generate order number
        import random
        import string
        order_number = 'ORD' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        order = Order(
            order_number=order_number,
            user_id=current_user,
            total_amount=total_amount,
            payment_method=data.get('payment_method', 'card'),
            shipping_address=data.get('shipping_address', '')
        )
        db.session.add(order)
        db.session.flush()
        
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                size=cart_item.size
            )
            db.session.add(order_item)
        
        Cart.query.filter_by(user_id=current_user).delete()
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating order', 'error': str(e)}), 500

@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        current_user = get_jwt_identity()
        orders = Order.query.filter_by(user_id=current_user).order_by(Order.created_at.desc()).all()
        
        return jsonify({'orders': [order.to_dict() for order in orders]})
    except Exception as e:
        return jsonify({'message': 'Error fetching orders', 'error': str(e)}), 500

# Initialize database and create sample data
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default categories
        categories = [
            'One Piece', 'Naruto', 'Attack on Titan', 'My Hero Academia',
            'One Punch Man', 'Demon Slayer', 'Black Clover', 'Dragon Ball',
            'Jujutsu Kaisen', 'Solo Leveling', 'Accessories'
        ]
        
        for cat_name in categories:
            if not Category.query.filter_by(name=cat_name).first():
                category = Category(name=cat_name)
                db.session.add(category)
        
        # Create sample products if none exist
        if Product.query.count() == 0:
            sample_products = [
                {
                    "name": "Monkey D. Luffy Costume",
                    "description": "Complete Luffy costume with straw hat, red vest, and blue shorts.",
                    "price": 2499,
                    "image_url": "https://hokagestore.com/wp-content/uploads/2018/09/33012-4a63aa.jpeg",
                    "sizes": ["S", "M", "L", "XL"],
                    "featured": True,
                    "badge": "Best Seller",
                    "category_name": "One Piece"
                },
                {
                    "name": "Naruto Uzumaki Costume",
                    "description": "Naruto's orange jumpsuit with Konoha headband and blonde wig.",
                    "price": 2199,
                    "image_url": "https://images.unsplash.com/photo-1632493563319-6c5be7025ecc",
                    "sizes": ["S", "M", "L", "XL"],
                    "featured": True,
                    "badge": "New",
                    "category_name": "Naruto"
                }
            ]
            
            for product_data in sample_products:
                category = Category.query.filter_by(name=product_data["category_name"]).first()
                if category:
                    product = Product(
                        name=product_data["name"],
                        description=product_data["description"],
                        price=product_data["price"],
                        image_url=product_data["image_url"],
                        sizes=product_data["sizes"],
                        featured=product_data["featured"],
                        badge=product_data["badge"],
                        category_id=category.id,
                        stock_quantity=50
                    )
                    db.session.add(product)
        
        db.session.commit()

# Initialize the database when the app starts
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)