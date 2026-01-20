# Gunicorn configuration for Render free tier
# Optimized for low memory (512 MB)

# Worker settings
workers = 1  # Single worker for low memory
worker_class = "sync"
threads = 1

# Timeout settings
timeout = 120  # Allow longer time for prediction
graceful_timeout = 30
keepalive = 5

# Memory optimization
max_requests = 100  # Restart worker after 100 requests to free memory
max_requests_jitter = 20

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Bind
bind = "0.0.0.0:10000"
