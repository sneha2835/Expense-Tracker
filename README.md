# 💰 AI-Powered Expense Tracker

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)

**Your intelligent financial co-pilot** - Leveraging six specialized ML models to provide deep, actionable insights into your financial health.


## 🔍 Core AI Models

### 1. Expense Predictor
- **Model**: Random Forest Regressor  
- **Function**: Forecasts category-wise spending patterns to enable proactive budget planning  
- **Inputs**: Historical spending, income patterns, lifestyle factors  
- **Output**: Predicted monthly expenses by category  

### 2. Overspending Alert System  
- **Model**: XGBoost Classifier  
- **Function**: Monitors real-time spending against budget thresholds  
- **Inputs**: Current expenditures vs. budget allocations  
- **Output**: Instant notifications when approaching budget limits  

### 3. Anomaly Detector  
- **Model**: Isolation Forest  
- **Function**: Identifies unusual financial transactions  
- **Inputs**: Transaction patterns, spending frequency, amount deviations  
- **Output**: Flagged suspicious transactions  

### 4. Savings Efficiency Model  
- **Model**: Decision Tree  
- **Function**: Evaluates savings progress against goals  
- **Inputs**: Income vs. savings ratio, target benchmarks  
- **Output**: Savings efficiency percentage and improvement tips  

### 5. Financial Health Score  
- **Model**: Random Forest Regressor  
- **Function**: Computes comprehensive financial wellness score  
- **Inputs**: 12+ financial metrics including debt-to-income ratio  
- **Output**: 0-100 score with category breakdown  

### 6. Personalized Recommender  
- **Model**: Random Forest Regressor  
- **Function**: Generates customized spending/saving strategies  
- **Inputs**: User behavior patterns and financial goals  
- **Output**: Actionable optimization recommendations  

## 🛠 Tech Stack

### Core Components
| Layer | Technology |
|-------|------------|
| **Frontend** | Streamlit |
| **Backend** | Django REST Framework |
| **Database** | MySQL 8.0 |
| **Machine Learning** | Scikit-learn, XGBoost, Pandas |

### ML Models
| Model | Algorithm | Purpose |
|-------|-----------|---------|
| Expense Predictor | Random Forest Regressor | Forecast category-wise spending for budget planning |
| Overspending Alert | XGBoost Classifier | Monitor spending thresholds and trigger alerts |
| Anomaly Detector | Isolation Forest | Detect abnormal or suspicious expense behavior |
| Savings Efficiency Model | Decision Tree | Assess savings progress and calculate efficiency ratios |
| Financial Health Score | Random Forest Regressor | Generate comprehensive score using income/spending metrics |
| Personalized Recommender | Random Forest Regressor | Suggest user-specific spending/saving strategies |

## 🚀 Installation

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Git

### Setup Instructions

### 1. **Clone the repository**

git clone https://github.com/sneha2835/Expense-Tracker.git

cd AI-Powered-Expense-Tracker

### 2. **Set up virtual environment**

python -m venv venv

source venv/bin/activate  # Linux/Mac

venv\Scripts\activate     # Windows

### 3. **Configure MySQL Database**

CREATE DATABASE budget_db;

CREATE USER 'budget_user'@'localhost' IDENTIFIED BY 'secure_password';

GRANT ALL PRIVILEGES ON budget_db.* TO 'budget_user'@'localhost';

### **4.Install dependencies**

pip install -r requirements.txt

### 5. **Configure environment variables**

Go to settings.py file and change the following accordingly

DB_NAME=budget_db

DB_USER=budget_user

DB_PASSWORD=secure_password

DB_HOST=localhost

DB_PORT=3306

SECRET_KEY=your-django-secret-key

### 6. **Run database migrations**

python manage.py makemigrations

python manage.py migrate


### 7. **Start the application**

> Backend (Django)
> 
python manage.py runserver

> Frontend (Streamlit) - in new terminal

cd frontend

streamlit run app.py

### 1. Homepage

<img width="1970" height="1144" alt="image" src="https://github.com/user-attachments/assets/6b71cd8c-ce4a-411d-9a8f-9d95d91f5796" />

### 2. Expense Prediction

<img width="1415" height="1043" alt="image" src="https://github.com/user-attachments/assets/fcee46be-206e-4a06-8fe6-5bd9a04f9e6a" />

### 3. Anomaly Detection

<img width="1496" height="1043" alt="image" src="https://github.com/user-attachments/assets/e560967b-689a-41c1-a14b-d04209712e15" />

### 4. Financial Health Score

<img width="1462" height="500" alt="image" src="https://github.com/user-attachments/assets/1235b425-8328-4dcf-ad67-8a07c5502b8a" />

### 5. Savings Efficiency 

<img width="1462" height="500" alt="image" src="https://github.com/user-attachments/assets/365c0285-56ea-4af4-9d57-dca51ab6798a" />

### 6. Personalized Recommendations

<img width="1462" height="500" alt="image" src="https://github.com/user-attachments/assets/7e2edc0c-65df-457d-b290-31e4186b6f67" />

### 7. Overspending Alerts

<img width="1442" height="596" alt="image" src="https://github.com/user-attachments/assets/b7e2ca26-fa5e-4a81-af26-09b8363c4e83" />

## 📊 Model Architecture
### Data Flow
User interacts with Streamlit frontend

Frontend sends API requests to Django backend

Django queries MySQL database

Appropriate ML model processes the data

Results are returned to frontend for visualization

### Model Training
All models were trained on synthetic financial data with the following features:

Income levels

Expense categories (rent, groceries, entertainment)

Savings rates

Historical spending patterns

### 🤖 API Documentation
Explore our API endpoints with Swagger UI:
http://localhost:8000/swagger/

Sample request:

import requests

headers = {"Authorization": "Bearer YOUR_TOKEN"}
response = requests.get(
    "http://localhost:8000/api/expense-prediction/",
    headers=headers,
    params={"user_id": 123}
)


### 🌱 Future Enhancements

Real-time bank integration via Plaid API

Mobile application with React Native

Advanced visualizations with D3.js

Predictive budgeting with LSTM networks

Multi-currency support for global users

### 🤝 Contributing

We welcome contributions! Please follow these steps:

Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add some amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request


### 📞 Contact

Email: snehakamatam28@gmail.com

GitHub: github.com/sneha2835
