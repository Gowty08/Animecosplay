// Product API
window.ProductAPI = {
    fetchAllProducts: async function() {
        try {
            const response = await fetch('/api/products');
            return await response.json();
        } catch (error) {
            console.error('Error fetching products:', error);
            return {};
        }
    },
    
    fetchProductsByCategory: async function(category) {
        try {
            const response = await fetch(`/api/products/${category}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching products by category:', error);
            return {};
        }
    },
    
    fetchProduct: async function(productId) {
        try {
            const response = await fetch(`/api/product/${productId}`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching product:', error);
            return null;
        }
    }
};

// Product Utilities
window.ProductUtils = {
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
    
    formatPrice: function(price) {
        return `₹${price.toLocaleString()}`;
    }
};

// Initialize empty objects if they don't exist (for safety)
if (!window.AuthService) window.AuthService = { currentUser: null };
if (!window.CartManager) window.CartManager = { getCart: () => [] };
if (!window.WishlistManager) {
    window.WishlistManager = { 
        getWishlist: () => [], 
        isInWishlist: () => false 
    };
}