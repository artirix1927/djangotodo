FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    libffi-dev \
    musl-dev \
    python3-dev \
    && rm -rf /var/cache/apk/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir gunicorn \
    && pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput

# Expose the port for the Django app
EXPOSE 8000

# Run Gunicorn with two workers
CMD ["gunicorn","--chdir","/app/todo/", "--bind", "0.0.0.0:8000", "--workers", "2", "todo.wsgi:application"]
