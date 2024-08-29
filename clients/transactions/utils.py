from decimal import Decimal

def convert_currency(amount, source_currency, target_currency):
    exchange_rates = {
        'USD': Decimal(1.00),
        'EUR': Decimal(0.85),
        'GBP': Decimal(0.75),
        'NGN': Decimal(750.00),
        'JPY': Decimal(110.50)
    }

    if source_currency not in exchange_rates or target_currency not in exchange_rates:
        raise ValueError("Invalid currency code.")
    
    amount_in_usd = amount / exchange_rates[source_currency]
    
    converted_amount = amount_in_usd * exchange_rates[target_currency]
    
    return converted_amount


