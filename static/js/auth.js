// Authentication Service
window.AuthService = {
    users: JSON.parse(localStorage.getItem('animeCosplayUsers')) || [],
    currentUser: JSON.parse(localStorage.getItem('animeCosplayCurrentUser')) || null,

    signup: function (userData) {
        const existingUser = this.users.find(user => user.email === userData.email);
        if (existingUser) {
            return { success: false, message: 'User with this email already exists' };
        }

        const newUser = {
            id: Date.now().toString(),
            ...userData,
            createdAt: new Date().toISOString(),
            orders: []
        };

        this.users.push(newUser);
        localStorage.setItem('animeCosplayUsers', JSON.stringify(this.users));

        return { success: true, user: newUser };
    },

    login: function (email, password) {
        const user = this.users.find(u => u.email === email && u.password === password);
        if (user) {
            this.currentUser = user;
            localStorage.setItem('animeCosplayCurrentUser', JSON.stringify(user));
            return { success: true, user };
        } else {
            return { success: false, message: 'Invalid email or password' };
        }
    },

    logout: function () {
        this.currentUser = null;
        localStorage.removeItem('animeCosplayCurrentUser');
    },

    updateProfile: function (userId, updates) {
        const userIndex = this.users.findIndex(u => u.id === userId);
        if (userIndex !== -1) {
            this.users[userIndex] = { ...this.users[userIndex], ...updates };
            localStorage.setItem('animeCosplayUsers', JSON.stringify(this.users));

            if (this.currentUser && this.currentUser.id === userId) {
                this.currentUser = this.users[userIndex];
                localStorage.setItem('animeCosplayCurrentUser', JSON.stringify(this.currentUser));
            }

            return { success: true, user: this.users[userIndex] };
        }
        return { success: false, message: 'User not found' };
    },

    addOrder: function (userId, order) {
        const userIndex = this.users.findIndex(u => u.id === userId);
        if (userIndex !== -1) {
            const newOrder = {
                id: `ORD${Date.now()}`,
                ...order,
                date: new Date().toISOString(),
                status: 'pending' // Default status
            };

            this.users[userIndex].orders.unshift(newOrder);
            localStorage.setItem('animeCosplayUsers', JSON.stringify(this.users));

            if (this.currentUser && this.currentUser.id === userId) {
                this.currentUser.orders.unshift(newOrder);
                localStorage.setItem('animeCosplayCurrentUser', JSON.stringify(this.currentUser));
            }

            return { success: true, order: newOrder };
        }
        return { success: false, message: 'User not found' };
    }
};