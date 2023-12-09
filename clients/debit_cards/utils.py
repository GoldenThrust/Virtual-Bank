import hashlib
import random


def luhn_checksum(card_number):
    digits = [int(x) for x in card_number]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for digit in even_digits:
        checksum += sum(divmod(digit * 2, 10))
    return checksum % 10

def generate_valid_credit_card_number():
    '''
    Generate a random credit card number using the Luhn algorithm.

    Returns:
    - str: A valid 16-digit credit card number with a starting digit '5'.
    '''
    card_number = '5' + ''.join(str(random.randint(0, 9)) for _ in range(13))
    
    checksum = luhn_checksum(card_number)
    
    while checksum != 0:
        card_number = '5' + ''.join(str(random.randint(0, 9)) for _ in range(13))
        checksum = luhn_checksum(card_number)

    return card_number

def generate_cvv(card_number, expiration_date):
    '''
    Generate a simulated CVV based on the provided card number and expiration date.

    Args:
    - card_number (str): The card number to generate CVV from.
    - expiration_date (datetime.datetime): The expiration date of the card.

    Returns:
    - str: The simulated CVV code.
    '''
    formatted_date = expiration_date.strftime('%d%m')
    
    card_number_int = int(card_number)
    
    masked_card_number = card_number_int >> 5
    
    combined_data = int(f'{formatted_date}{masked_card_number}')
    
    masked_combined_data = combined_data & card_number_int
    
    hashed = hashlib.sha256(str(masked_combined_data).encode()).hexdigest()

    cvv = []
    index = 0
    for char in hashed[::-5]:
        index += 1
        try:
            int_value = int(char)
            
            if len(cvv) < 3:
                cvv.append(char)
        except ValueError:
            pass
    
    return ''.join(cvv)
