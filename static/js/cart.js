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
            cart.push({ ...product, quantity, size });
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
            wishlist.push(product);
            localStorage.setItem('animeCosplayWishlist', JSON.stringify(wishlist));
        }
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
    }
};