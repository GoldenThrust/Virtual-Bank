from datetime import datetime

afr = "10/23"

class DateError(Exception):
    pass

try:
    month, year = afr.split('/')
    month = int(month)
    year = int(f'20{year}')

    current_year = datetime.now().year
    current_month = datetime.now().month

    if not (1 <= month <= 12):
        raise DateError("Invalid month")
    elif year < current_year or (year == current_year and month < current_month):
        raise DateError("Card has expired")
    elif not (year <= 2099):
        raise DateError("Invalid year")
    else:
        print("Valid month and year")
except DateError as e:
    print(e.message)
except Exception:
    print("invalid expiry date")
