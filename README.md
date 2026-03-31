# EliteMess CMS 🍱🛡️

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**EliteMess CMS** is a premium, enterprise-grade Mess Management System designed to streamline mess operations, automate billing, and provide a high-end experience for students and staff. Engineered with a robust Django/PostgreSQL backend and a modern glassmorphism UI.

---

## 🌟 Key Features

### 👨‍🎓 Student Dashboard
- **Live Menu**: Real-time view of daily mess offerings.
- **Feedback Loop**: Direct channel to share and view mess feedback.
- **Automated Billing**: Monthly bills generated automatically based on attendance logs.
- **Dynamic Payments**: Integrated QR code generation for seamless UPI payments.

### 👨‍💼 Staff & Control Center
- **Excel Automation**: Bulk attendance processing via `.xlsx` uploads using Pandas & Openpyxl.
- **Payment Verification**: Dedicated queue for verifying student payment receipts.
- **Menu Management**: Real-time editor for daily mess schedules.
- **Advanced Admin**: Custom Django Admin branding for high-level management.

### 🔒 Security & UX
- **Intelligent Exception Handling**: Custom CSRF recovery and Toast notifications for all system events.
- **Role-Based Access**: Strict session management ensuring students and staff see only their relevant data.

---

## 🛠️ Technical Stack

- **Backend**: Python 3.12, Django 6.0.3
- **Database**: PostgreSQL 18 (Relational storage)
- **Data Processing**: Pandas, OpenPyXL (Excel automation)
- **Frontend**: Vanilla JS (Dynamic Toasts, QR generation), CSS3 (Glassmorphism design system)
- **Environment**: `django-environ` for secure configuration.

---

## 🚀 Quick Setup

### 1. Prerequisites
- Python 3.12+
- PostgreSQL 18

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/sarangwagh04/Elite-Mess.git
cd Elite-Mess

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/elitemess_db
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Launch
```bash
python manage.py runserver
```

---

## 👨‍💻 Developer Profile

**Sarang Wagh**  
*BE in Computer Science & Design*  
**Vithalrao Vikhe Patil College of Engineering, Ahilyanagar**

[LinkedIn](https://linkedin.com/in/sarang-wagh) | [GitHub](https://github.com/sarangwagh04)

---
&copy; 2026 EliteMess CMS. All rights reserved.
