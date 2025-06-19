import os

def api_url_config(request):
    """
    Adds API_URL to the template context so it can be used in all templates.
    """
    api_url = os.environ.get('API_URL')
    
    if not api_url:
        api_host = os.environ.get('API_HOST', 'localhost')
        api_port = os.environ.get('API_PORT', '8030')
        api_url = f"http://{api_host}:{api_port}"
    
    api_url = api_url.rstrip('/')
    
    return {
        'API_URL': api_url,
    }
