# Gunicorn configuration for Railway
# Optimized for Railway's resources

# Worker settings
workers = 1
worker_class = "sync"
threads = 2

# Timeout
timeout = 120
graceful_timeout = 30
keepalive = 5

# Memory optimization
max_requests = 100
max_requests_jitter = 20

# Preload app to share memory
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Note: bind is set via command line --bind 0.0.0.0:$PORT in Procfile
