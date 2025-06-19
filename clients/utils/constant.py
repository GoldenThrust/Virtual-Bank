import os

# Get API URL from environment or use default
api_url = os.environ.get("API_URL", "http://localhost:8030").rstrip("/") + "/"