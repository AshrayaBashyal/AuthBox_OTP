# 1️⃣ Base image (lightweight Linux + Python)
FROM python:3.11-slim

# 2️⃣ Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Set working directory inside container
WORKDIR /app

# 4️⃣ Install system dependencies (for psycopg2 later)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5️⃣ Copy requirements first (caching trick)
COPY requirements.txt .

# 6️⃣ Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# 7️⃣ Copy rest of the project
COPY . .

# 8️⃣ Default command (run Django)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
