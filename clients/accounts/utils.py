import random
from django.core.serializers import serialize
import json
from .models import Account

def generate_account_number():
    return "".join(str(random.randint(0, 9)) for _ in range(12))

def update_account(account, session):
    if account:
        if (isinstance(account, dict)):
            account = Account.objects.filter(pk=account['pk']).first()
        else:
            account = Account.objects.filter(pk=account.pk).first()

        serialized_account = serialize('json', [account])
        deserialized_account = json.loads(serialized_account)
        session["account"] = deserialized_account[0]['fields']
        session["account"]['pk'] = deserialized_account[0]['pk']