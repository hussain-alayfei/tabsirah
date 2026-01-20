# Gunicorn configuration for Render free tier
# Optimized for VERY low memory (512 MB, 0.1 CPU)

# Worker settings - minimal
workers = 1
worker_class = "sync"
threads = 1

# Timeout - shorter to prevent hanging
timeout = 30
graceful_timeout = 10
keepalive = 2

# Memory optimization - aggressive
max_requests = 50  # Restart worker frequently to free memory
max_requests_jitter = 10

# Preload app to share memory
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "warning"

# Bind
bind = "0.0.0.0:10000"
