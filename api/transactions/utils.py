def convert_currency(amount, source_currency, target_currency):
    exchange_rates = {
        'USD': 1.00,
        'EUR': 0.85,
        'GBP': 0.75,
        'NGN': 750.00,
        'JPY': 110.50
    }

    if source_currency not in exchange_rates or target_currency not in exchange_rates:
        raise ValueError("Invalid currency code.")
    
    amount_in_usd = amount / exchange_rates[source_currency]
    
    converted_amount = amount_in_usd * exchange_rates[target_currency]
    
    return converted_amount


