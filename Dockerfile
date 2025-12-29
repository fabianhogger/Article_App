# Use Python 3.9 slim image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Download required NLTK and spaCy data
RUN python -m nltk.downloader stopwords punkt vader_lexicon && \
    python -m spacy download en_core_web_sm

# Copy project files
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/main/media /app/main/static

# Expose port
EXPOSE 8000

# Set working directory to main (where manage.py is located)
WORKDIR /app/main

# Run migrations and start server
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    python manage.py runserver 0.0.0.0:8000
