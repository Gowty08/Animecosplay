# AnimeCosplay - E-Commerce Web Application

A lightweight and modern **Python-based e-commerce web app** with a dynamic frontend and RESTful backend.  
This project demonstrates a full web stack with product management, cart functionality, authentication, and order handling.

---

## Features

-  Dynamic product rendering from `products.json`
-  Shopping cart and wishlist functionality
-  User authentication (login, account, checkout)
-  Order success and tracking page
-  Responsive UI built with HTML, CSS, and JS
-  Easy setup using `venv` and `requirements.txt`

---

## Project Structure

``` bash
.
├── app.py
├── data
│   └── products.json
├── index.html
├── package.Json
├── package-lock.json
├── README.md
├── requirements.txt
├── runtime.txt
├── static
│   ├── css
│   │   ├── responsive.css
│   │   └── style.css
│   └── js
│       ├── auth.js
│       ├── cart.js
│       └── products.js
└── templates
    ├── account.html
    ├── base.html
    ├── cart.html
    ├── checkout.html
    ├── home.html
    ├── login.html
    ├── order-success.html
    ├── product-details.html
    └── wishlist.html

5 directories, 22 files
```

---

## Prerequisites

Make sure you have the following installed:

- **Python 3.8+**
- **pip** (Python package manager)
- **virtualenv** (recommended)

---

## Setup Instructions

1. **Clone this repository**

   ```bash
   git clone https://github.com/Gowty08/Animecosplay.git
   cd Animecosplay
    ```

2. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```


4. **Run the application**

```bash
python3 app.py
```


5. **Open your browser**

```arduino

http://localhost:5000

```

--- 


##  Project Details

Backend	Python (Flask)
Frontend - HTML, CSS, JS (vanilla)
Data - JSON-based product storage
Static Assets - Managed in static/ folder
Templates - Jinja2 templates for pages

##  Deployment

To deploy this app (for example on Render, Heroku, or Railway):
Ensure runtime.txt specifies your Python version (e.g., python-3.11.0).

- Make sure requirements.txt is up-to-date:

```bash

pip freeze > requirements.txt
```

### Push your code to a remote Git repository.

- Configure the deployment platform to start with:

```bash
python3 app.py
```
