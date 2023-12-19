from django import template
register = template.Library()

@register.filter
def currency_to_unicode(currency_code):
    currency_mapping = {
        "USD": "&#36;",  # US Dollar
        "EUR": "&#8364;",  # Euro
        "GBP": "&#163;",  # British Pound
        "NGN": "&#8358;",  # Nigerian Naira
    }

    return currency_mapping.get(currency_code, "")