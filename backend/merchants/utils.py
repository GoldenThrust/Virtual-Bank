from .models import Merchant

def get_url():
    allowed_urls = Merchant.objects.values_list('website_url', flat=True)

    with open('.url_file', 'w') as f:
        f.writelines('\n'.join(allowed_urls))