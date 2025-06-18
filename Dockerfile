FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Fix the syntax error in apt-get install
RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd -m appuser

# Install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY --chown=appuser:appuser . .

# Switch to appuser
USER appuser

# Set working directory for API
WORKDIR /app/api

# Run collectstatic (comment out if using volumes in development)
RUN python manage.py collectstatic --noinput

# Expose port for the application
EXPOSE 8030

# Set the entrypoint script
COPY --chown=appuser:appuser docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Default command (can be overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8030"]
