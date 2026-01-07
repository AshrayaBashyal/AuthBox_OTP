AuthBox_OTP

AuthBox_OTP is a modular Django backend project providing secure user authentication with email & OTP verification. It leverages Celery + Redis for asynchronous tasks, email notifications, and JWT-based authentication.

Features

Custom user model with email login

OTP-based verification system

Email notifications via SMTP

Asynchronous task processing with Celery + Redis

JWT authentication (access & refresh tokens)

Modular app structure for users, emails, and OTP

Production-ready configuration using .env

Installation

Clone the repo:

git clone https://github.com/yourusername/AuthBox_OTP.git
cd AuthBox_OTP


Create & activate a virtual environment:

python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate  # macOS/Linux


Install dependencies:

pip install -r requirements.txt


Configure .env with your settings (email, database, JWT, Celery, Redis).

Usage

Run Django migrations:

python manage.py migrate


Start the development server:

python manage.py runserver


Start Celery worker:

celery -A authbox worker -l info


Optional: start Celery beat for scheduled tasks:

celery -A authbox beat -l info

Project Structure
authbox/
├─ manage.py
├─ authbox/          # Django project settings
├─ celery.py         # Celery configuration
├─ apps/
│  ├─ users/         # User model, serializers, views, urls
│  ├─ emails/        # Email services
│  └─ otp/           # OTP utils and tasks
├─ requirements.txt
├─ .env              # Environment variables
