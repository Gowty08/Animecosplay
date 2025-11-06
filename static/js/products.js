// Product API
window.ProductAPI = {
    fetchAllProducts: async function() {
        try {
            const response = await fetch('/api/products');
            const data = await response.json();
            
            // Convert the new structure to flat products array for backward compatibility
            if (data.categories) {
                const allProducts = [];
                data.categories.forEach(category => {
                    category.products.forEach(product => {
                        allProducts.push({
                            ...product,
                            // Ensure consistent image property name
                            image: product.image || product.imageUrl
                        });
                    });
                });
                return allProducts;
            }
            return data;
        } catch (error) {
            console.error('Error fetching products:', error);
            return [];
        }
    },
    
    fetchProductsByCategory: async function(category) {
        try {
            const response = await fetch('/api/products');
            const data = await response.json();
            
            if (data.categories) {
                const categoryData = data.categories.find(cat => cat.id === category);
                if (categoryData) {
                    return categoryData.products.map(product => ({
                        ...product,
                        image: product.image || product.imageUrl
                    }));
                }
            }
            return [];
        } catch (error) {
            console.error('Error fetching products by category:', error);
            return [];
        }
    },
    
    fetchProduct: async function(productId) {
        try {
            const response = await fetch('/api/products');
            const data = await response.json();
            
            if (data.categories) {
                for (let category of data.categories) {
                    const product = category.products.find(p => p.id === productId);
                    if (product) {
                        return {
                            ...product,
                            image: product.image || product.imageUrl
                        };
                    }
                }
            }
            return null;
        } catch (error) {
            console.error('Error fetching product:', error);
            return null;
        }
    },
    
    // New method to fetch categories
    fetchCategories: async function() {
        try {
            const response = await fetch('/api/products');
            const data = await response.json();
            return data.categories || [];
        } catch (error) {
            console.error('Error fetching categories:', error);
            return [];
        }
    },
    
    // New method to fetch featured products
    fetchFeaturedProducts: async function() {
        try {
            const response = await fetch('/api/products');
            const data = await response.json();
            
            if (data.categories) {
                const featuredProducts = [];
                data.categories.forEach(category => {
                    category.products.forEach(product => {
                        if (product.featured) {
                            featuredProducts.push({
                                ...product,
                                image: product.image || product.imageUrl
                            });
                        }
                    });
                });
                return featuredProducts;
            }
            return [];
        } catch (error) {
            console.error('Error fetching featured products:', error);
            return [];
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
    },
    
    // New utility to get category name by ID
    getCategoryName: function(categories, categoryId) {
        const category = categories.find(cat => cat.id === categoryId);
        return category ? category.name : 'Unknown Category';
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