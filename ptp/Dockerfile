FROM python:3.11 AS djangobase

ENV USER=ptp

RUN mkdir /app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc git-lfs python3-dev redis-server supervisor \
    && apt-get clean

# Install Java (OpenJDK)
RUN apt-get update && apt-get install -y openjdk-17-jre-headless \
    && apt-get clean

# Set JAVA_HOME environment variable (optional)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy the application code
FROM djangobase AS djangoapp

COPY . /app/

WORKDIR /app

# Expose the port the Django app runs on
EXPOSE 8000

RUN useradd -u 1000 $USER

RUN chown -R $USER:$USER /etc/supervisor/conf.d/supervisord.conf
RUN chown -R $USER:$USER /app/
RUN chown -R $USER:$USER /var/log/supervisor/
RUN chmod +x /app/start-script.sh
RUN chmod +x /app/start-django.sh

# Make sure the container is running as non-root
USER $USER

ENV CELERY_BROKER_URL="redis://localhost:6379/0"
ENV REDIS_URL="redis://localhost:6379/0"
ENV MODEL_DIR = "/app/inference/models/models"
# Models will be downloaded and placed in /app/inference/models/models through SciLifeLab Serve interface

# Start supervisord
CMD ["sh", "-c", "/app/start-script.sh"]
