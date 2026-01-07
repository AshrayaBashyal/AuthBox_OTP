# 🔐 AuthBox_OTP

**AuthBox_OTP** is a modular authentication backend built with **Django + Django REST Framework**, designed for modern applications.  
It provides secure user management with **email + OTP verification**, **JWT authentication**, and asynchronous task handling via **Celery + Redis**.

---

## 🚀 Features

- User registration & login with custom user model  
- JWT authentication (access & refresh tokens)  
- OTP-based email verification system  
- Password reset & secure token handling  
- Asynchronous tasks via Celery + Redis  
- Email notifications via SMTP  
- Modular structure for users, emails, and OTP  
- Production-ready configuration using `.env`

---

## 🛠 Tech Stack

- Python 3.13  
- Django 6.x  
- Django REST Framework  
- PostgreSQL (for production, optional SQLite for dev)  
- JWT Authentication  
- SMTP Email (Gmail or custom SMTP)  
- Celery + Redis for background tasks

---

## 🔒 Security

All secrets are stored using **environment variables**.  

Never commit the following to Git:

- `SECRET_KEY`  
- Database credentials  
- Email passwords  

These should go into a `.env` file (already excluded in `.gitignore`).

---

## ⚡ Setup (Local)

1. Clone the repository:

```
git clone https://github.com/AshrayaBashyal/AuthBox_OTP.git
cd AuthBox_OTP
```
2. Create & activate a virtual environment:
```
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create a .env file with:
```
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
REDIS_URL=redis://localhost:6379/0
JWT_SIGNING_KEY=your-jwt-key
```

5. Run Django migrations:
```
python manage.py migrate
```
6. Start development server:
```
python manage.py runserver
```
7. Start Celery worker:
```
celery -A authbox worker -l info
```
8. Optional: start Celery beat for scheduled tasks:
```
celery -A authbox beat -l info
```
9. Make sure Redis server is running
```
redis-server
```

---

## 📁 Project Structure
```
AuthBox_OTP/
├─ manage.py
├─ authbox/              # Django project settings
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
├─ celery.py             # Celery configuration
├─ apps/
│  ├─ users/             # User model, serializers, views, urls
│  │  ├─ __init__.py
│  │  ├─ models.py
│  │  ├─ serializers.py
│  │  ├─ views.py
│  │  ├─ urls.py
│  │  └─ tasks.py
│  ├─ emails/            # Email services
│  │  ├─ __init__.py
│  │  └─ services.py
│  └─ otp/               # OTP utils and tasks
│     ├─ __init__.py
│     ├─ utils.py
│     └─ tasks.py
├─ requirements.txt
└─ .env                  # Environment variables
```