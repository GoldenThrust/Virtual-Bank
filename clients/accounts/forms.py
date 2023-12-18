from django import forms
from .models import Account
from .utils import generate_account_number

class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            "name",
            "account_type",
            "currency",
        ]

    def save(self, commit=True, request=None):
        print(request)

        instance = super().save(commit=False)
        instance.user_id = request.user.pk 
        instance.number = generate_account_number()

        if commit:
            instance.save()
        return instance