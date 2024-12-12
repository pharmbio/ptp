FROM python:3.11 AS djangobase

ENV USER=ptp

RUN mkdir /app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc git-lfs python3-dev redis-server supervisor nginx \
    && apt-get clean

# Install Java (OpenJDK)
RUN apt-get update && apt-get install -y openjdk-17-jre-headless \
    && apt-get clean

RUN mkdir -p /var/lib/nginx/body
RUN chown -R www-data:www-data /var/lib/nginx
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
RUN mkdir -p /app/ext_storage/
# Models also need to be added. They be downloaded and placed in /app/ext_storage/models/ through the SciLifeLab Serve interface

# Expose the port the Django app runs on
EXPOSE 8000

RUN useradd -u 1000 $USER

RUN chown -R $USER:$USER /etc/supervisor/conf.d/supervisord.conf
RUN chown -R $USER:$USER /app/
RUN chown -R $USER:$USER /var/log/supervisor/
RUN chown -R $USER:$USER /var/lib/nginx/
RUN chown -R $USER:$USER /var/log/nginx/
RUN chmod +x /app/start-script.sh
RUN chmod +x /app/start-django.sh

# Make sure the container is running as non-root
USER $USER

# Start supervisord
CMD ["sh", "-c", "/app/start-script.sh"]
