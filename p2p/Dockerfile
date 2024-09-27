FROM python:3.11 AS djangobase

# Set working directory

RUN mkdir /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the application code
FROM djangobase AS djangoapp

COPY . /app/

WORKDIR /app



# Expose the port the Django app runs on
EXPOSE 8000

# Default command
CMD ["gunicorn", "p2p.wsgi:application", "--bind", "0.0.0.0:8000"]