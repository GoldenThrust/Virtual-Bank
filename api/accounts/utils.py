import random

def generate_account_number():
    return "".join(str(random.randint(0, 9)) for _ in range(12))

def currency_to_unicode(currency_code):
    currency_mapping = {
        "USD": "$",   # US Dollar
        "EUR": "€", # Euro
        "GBP": "£",  # British Pound
        "NGN": "₦", # Nigerian Naira
        "JPY": "¥",  # Japanese Yen
    }


    return currency_mapping.get(currency_code, "")