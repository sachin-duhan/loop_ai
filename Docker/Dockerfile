# Base image
FROM python:latest

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY ../ .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    # Install supervisor, Redis server, and PostgreSQL
    apt-get update && apt-get install -y supervisor redis-server postgresql && \
    # Making supervisord log path
    mkdir -p /var/log/supervisor/

# Copy the supervisor configuration file
COPY ../supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the necessary ports
EXPOSE 5000

# Start the supervisor service, Redis server, and PostgreSQL
CMD ["/bin/bash", "-c", "/etc/init.d/redis-server start && /etc/init.d/postgresql start && /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf"]
