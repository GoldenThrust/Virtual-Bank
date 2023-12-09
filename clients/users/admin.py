from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "User Address",
            {
                "fields": (
                    "address",
                    "city",
                    "state",
                    "country",
                )
            },
        ),
        (
            "Additional Fields",
            {
                "fields": (
                    "date_of_birth",
                    "profile_picture",
                    "phone_number",
                    "ip_address",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        (
            "User Address",
            {
                "fields": (
                    "address",
                    "city",
                    "state",
                    "country",
                )
            },
        ),
        (
            "Additional Fields",
            {
                "fields": (
                    "date_of_birth",
                    "profile_picture",
                    "phone_number",
                    "ip_address",
                )
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)