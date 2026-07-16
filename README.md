# 📦 Smart Inventory Optimization System

### Smart Inventory Management & Demand Forecasting Platform

---

## 📖 Overview

Smart Inventory Optimization System is a Full Stack AI-powered web application designed to streamline inventory management for retail and warehouse businesses.

The system enables users to manage products, monitor inventory levels, analyze business insights, and predict future product demand using Machine Learning. It combines real-time inventory tracking with predictive analytics to minimize stock shortages and improve inventory planning.

Built using FastAPI, SQLite, HTML, CSS, JavaScript, and Scikit-learn, this project demonstrates practical implementation of Full Stack Development, REST APIs, Database Management, and Machine Learning.

---

# ✨ Features

- 📦 Product Management (CRUD Operations)
- 📊 Interactive Inventory Dashboard
- 📉 Low Stock Detection
- 💰 Inventory Value Tracking
- 📈 Analytics Dashboard
- 🤖 AI-Based Demand Prediction
- 📤 Excel Import & Export
- 🔐 Secure User Authentication
- ⚡ FastAPI REST APIs
- 📱 Responsive User Interface

---

# 🎯 Key Highlights

- Full Stack Web Application
- Machine Learning Integration
- REST API Development using FastAPI
- Interactive Business Dashboard
- Real-Time Inventory Monitoring
- Inventory Analytics
- Demand Forecasting
- Excel File Processing
- SQLite Database Management
- Modular Project Architecture

---

# 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Backend | FastAPI |
| Frontend | HTML5, CSS3, JavaScript |
| Database | SQLite |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Data Visualization | Plotly |
| Excel Processing | OpenPyXL |
| API Testing | Swagger UI |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```text
SMART-INVENTORY-OPTIMIZATION-SYSTEM
│
├── app/
│   ├── main.py                  # FastAPI application
│   ├── database.py              # Database operations
│   ├── model.py                 # ML model loading
│   ├── predict.py               # Demand prediction
│   └── mail.py                  # Email notifications
│
├── static/
│   ├── css/                     # Stylesheets
│   ├── js/                      # JavaScript files
│   └── images/                  # Images
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── forgot_password.html
│   ├── dashboard.html
│   ├── products.html
│   ├── analytics.html
│   └── prediction.html
│
├── data/
│   └── sales_data.csv
│
├── models/                      # Saved ML models
│
├── inventory.db                 # SQLite database
├── train_model.py               # Train ML model
├── generate_dataset.py          # Dataset generation
├── requirements.txt             # Python dependencies
├── render.yaml                  # Render deployment
├── .env                         # Environment variables
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Abhishek06786/Smart-Inventory-Optimization-System.git
```

### Open Project

```bash
cd Smart-Inventory-Optimization-System
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Windows**

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Project

```bash
uvicorn app.main:app --reload
```

### Open Browser

```
http://127.0.0.1:8000
```

---

# 📸 Screenshots

### Login Page

![Login](screenshots/login.png)

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Products

![Products](screenshots/products.png)

### Analytics

![Analytics](screenshots/analytics.png)

### Prediction

![Prediction](screenshots/prediction.png)

---

# 🚀 Future Improvements

- Barcode Scanner Integration
- QR Code Based Inventory Tracking
- Email Notifications
- Cloud Database Support
- Multi-user Role Management
- AI Sales Forecasting

---

## 👨‍💻 Author

**Abhishek Choubey**

- GitHub: https://github.com/Abhishek06786

- LinkedIn: https://www.linkedin.com/in/abhishek-choubey-9635082a5/

---


## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.