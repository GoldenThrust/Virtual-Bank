from django.contrib import admin
from .models import (DebitCard, DebitCardTransaction)
# Register your models here.

admin.site.register(DebitCard)
admin.site.register(DebitCardTransaction)