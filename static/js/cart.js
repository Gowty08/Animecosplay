// Cart Management
window.CartManager = {
    getCart: function() {
        return JSON.parse(localStorage.getItem('animeCosplayCart')) || [];
    },
    
    addToCart: function(product, size = 'M', quantity = 1) {
        const cart = this.getCart();
        const existingItem = cart.find(item => item.id === product.id && item.size === size);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            // Store only essential product info in cart to avoid data duplication
            const cartItem = {
                id: product.id,
                name: product.name,
                price: product.price,
                // Handle both imageUrl and image fields
                image: product.imageUrl || product.image,
                size: size,
                quantity: quantity,
                // Store additional info that might be needed
                category: product.category,
                inStock: product.inStock
            };
            cart.push(cartItem);
        }
        
        localStorage.setItem('animeCosplayCart', JSON.stringify(cart));
        return cart;
    },
    
    updateQuantity: function(productId, newQuantity) {
        const cart = this.getCart();
        const updatedCart = cart.map(item => 
            item.id === productId ? { ...item, quantity: newQuantity } : item
        );
        
        localStorage.setItem('animeCosplayCart', JSON.stringify(updatedCart));
        return updatedCart;
    },
    
    removeItem: function(productId) {
        const cart = this.getCart();
        const updatedCart = cart.filter(item => item.id !== productId);
        
        localStorage.setItem('animeCosplayCart', JSON.stringify(updatedCart));
        return updatedCart;
    },
    
    clearCart: function() {
        localStorage.removeItem('animeCosplayCart');
        return [];
    },
    
    getCartCount: function() {
        const cart = this.getCart();
        return cart.reduce((total, item) => total + item.quantity, 0);
    },
    
    // New method to get full product details for cart items
    getCartWithFullDetails: function() {
        const cart = this.getCart();
        
        // If products data is available globally, enrich cart items with full details
        if (window.productsData && window.productsData.categories) {
            const allProducts = window.productsData.categories.flatMap(category => category.products);
            
            return cart.map(cartItem => {
                const fullProduct = allProducts.find(p => p.id === cartItem.id);
                if (fullProduct) {
                    return {
                        ...cartItem,
                        // Add full product details but keep cart-specific info (size, quantity)
                        description: fullProduct.description,
                        rating: fullProduct.rating,
                        reviews: fullProduct.reviews,
                        badge: fullProduct.badge,
                        sizes: fullProduct.sizes,
                        inStock: fullProduct.inStock,
                        featured: fullProduct.featured,
                        // Ensure we have the correct image
                        image: cartItem.image || fullProduct.imageUrl || fullProduct.image
                    };
                }
                return cartItem;
            });
        }
        
        return cart;
    },
    
    // Calculate total price
    getTotalPrice: function() {
        const cart = this.getCart();
        return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    },
    
    // Calculate total items (different from count - counts unique items)
    getTotalItems: function() {
        const cart = this.getCart();
        return cart.length;
    }
};

// Wishlist Management
window.WishlistManager = {
    getWishlist: function() {
        return JSON.parse(localStorage.getItem('animeCosplayWishlist')) || [];
    },
    
    addToWishlist: function(product) {
        const wishlist = this.getWishlist();
        if (!wishlist.find(item => item.id === product.id)) {
            // Store only essential product info in wishlist
            const wishlistItem = {
                id: product.id,
                name: product.name,
                price: product.price,
                image: product.imageUrl || product.image,
                category: product.category,
                rating: product.rating,
                badge: product.badge
            };
            wishlist.push(wishlistItem);
        }
        localStorage.setItem('animeCosplayWishlist', JSON.stringify(wishlist));
        return wishlist;
    },
    
    removeFromWishlist: function(productId) {
        const wishlist = this.getWishlist();
        const updatedWishlist = wishlist.filter(item => item.id !== productId);
        
        localStorage.setItem('animeCosplayWishlist', JSON.stringify(updatedWishlist));
        return updatedWishlist;
    },
    
    isInWishlist: function(productId) {
        const wishlist = this.getWishlist();
        return wishlist.some(item => item.id === productId);
    },
    
    clearWishlist: function() {
        localStorage.removeItem('animeCosplayWishlist');
        return [];
    },
    
    // New method to get full product details for wishlist items
    getWishlistWithFullDetails: function() {
        const wishlist = this.getWishlist();
        
        // If products data is available globally, enrich wishlist items with full details
        if (window.productsData && window.productsData.categories) {
            const allProducts = window.productsData.categories.flatMap(category => category.products);
            
            return wishlist.map(wishlistItem => {
                const fullProduct = allProducts.find(p => p.id === wishlistItem.id);
                if (fullProduct) {
                    return {
                        ...wishlistItem,
                        // Add full product details
                        description: fullProduct.description,
                        reviews: fullProduct.reviews,
                        sizes: fullProduct.sizes,
                        inStock: fullProduct.inStock,
                        featured: fullProduct.featured,
                        // Ensure we have the correct image
                        image: wishlistItem.image || fullProduct.imageUrl || fullProduct.image
                    };
                }
                return wishlistItem;
            });
        }
        
        return wishlist;
    }
};

// Product Utilities
window.ProductUtils = {
    // Render star ratings
    renderStars: function(rating) {
        const stars = [];
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;

        for (let i = 0; i < fullStars; i++) {
            stars.push(React.createElement('i', { key: i, className: "fas fa-star" }));
        }

        if (hasHalfStar) {
            stars.push(React.createElement('i', { key: "half", className: "fas fa-star-half-alt" }));
        }

        const emptyStars = 5 - stars.length;
        for (let i = 0; i < emptyStars; i++) {
            stars.push(React.createElement('i', { key: `empty-${i}`, className: "far fa-star" }));
        }

        return stars;
    },
    
    // Find product by ID in the nested structure
    findProductById: function(productId) {
        if (!window.productsData || !window.productsData.categories) return null;
        
        const allProducts = window.productsData.categories.flatMap(category => category.products);
        return allProducts.find(product => product.id === productId);
    },
    
    // Get products by category
    getProductsByCategory: function(categoryId) {
        if (!window.productsData || !window.productsData.categories) return [];
        
        const category = window.productsData.categories.find(cat => cat.id === categoryId);
        return category ? category.products : [];
    },
    
    // Get all featured products
    getFeaturedProducts: function() {
        if (!window.productsData || !window.productsData.categories) return [];
        
        const allProducts = window.productsData.categories.flatMap(category => category.products);
        return allProducts.filter(product => product.featured);
    },
    
    // Get all categories
    getCategories: function() {
        return window.productsData ? window.productsData.categories : [];
    }
};