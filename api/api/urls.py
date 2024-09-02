from django.urls import path

from users import views as users_views
from accounts import views as accounts_views
from debit_cards import views as debit_cards_views
from notifications import views as notifications_views

from transactions import views as transactions_views
from .views import ListApiUrls

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Virtual Bank API",
        default_version='v1',
        description="The Virtual Bank API is a RESTful API that provides endpoints for managing users, accounts, transactions, deposits, debit cards, transfers, and notifications. The API uses JWT authentication for securing certain endpoints and provides real-time transaction updates via WebSocket using Django Channels.",
        terms_of_service="https://www.google.com/policies/terms/",
        authentication_classes=('rest_framework_simplejwt.authentication.JWTAuthentication',),
        contact=openapi.Contact(email="adenijiolajid01@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


app_name = "api"

urlpatterns = [
    path("", ListApiUrls.as_view(), name="api_overview"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # User management (admin only)
    path("admin/users/", users_views.UserList.as_view(), name="admin_user_list"),
    path(
        "admin/users/<int:pk>/",
        users_views.UserDetail.as_view(),
        name="admin_user_detail",
    ),
    # Account management (admin only)
    path(
        "admin/accounts/",
        accounts_views.AccountList.as_view(),
        name="admin_account_list",
    ),
    path(
        "admin/accounts/<int:pk>/",
        accounts_views.AccountDetail.as_view(),
        name="admin_account_detail",
    ),
    # Debit cards management (admin only)
    path(
        "admin/debit-cards/",
        debit_cards_views.DebitCardList.as_view(),
        name="admin_debit_card_list",
    ),
    path(
        "admin/debit-cards/<int:pk>/",
        debit_cards_views.DebitCardDetail.as_view(),
        name="admin_debit_card_detail",
    ),
    # Notifications management (admin only)
    path(
        "admin/notifications/",
        notifications_views.NotificationList.as_view(),
        name="admin_notification_list",
    ),
    path(
        "admin/notifications/<int:pk>/",
        notifications_views.NotificationDetail.as_view(),
        name="admin_notification_detail",
    ),
    # Transactions management (admin only)
    path(
        "admin/transactions/",
        transactions_views.TransactionListAdmin.as_view(),
        name="admin_transaction_list",
    ),
    path(
        "admin/transactions/<int:pk>/",
        transactions_views.TransactionDetailAdmin.as_view(),
        name="admin_transaction_detail",
    ),
    # Public user API (no authorization required for some endpoints)
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verification"),
    path("auth/register/", users_views.UserCreate.as_view(), name="user_registration"),
    path("auth/update/", users_views.UserUpdate.as_view(), name="user_update"),
    path("auth/verify/", users_views.UserGet.as_view(), name="user_verification"),
    path("auth/login/", users_views.Login.as_view(), name="user_login"),
    path(
        "auth/token/refresh/",
        users_views.RefreshTokenView.as_view(),
        name="token_refresh",
    ),
    path("auth/logout/", users_views.Logout.as_view(), name="user_logout"),
    # Public account API
    path(
        "accounts/", accounts_views.UserAccountList.as_view(), name="account_list"
    ),
    path(
        "accounts/create/",
        accounts_views.AccountCreate.as_view(),
        name="account_creation",
    ),
    path(
        "accounts/<int:number>/",
        accounts_views.UserAccountDetail.as_view(),
        name="account_detail",
    ),
    # Public debit card API
    path(
        "debit-cards/",
        debit_cards_views.UserDebitCardList.as_view(),
        name="debit_card_list",
    ),
    path(
        "debit-cards/<int:number>/<int:cvv>/",
        debit_cards_views.UserDebitCardDetail.as_view(),
        name="debit_card_detail",
    ),
    path(
        "debit-cards/transactions/",
        transactions_views.DebitCardHistory.as_view(),
        name="debit_card_transactions_history",
    ),
    path(
        "debit-cards/transactions/<uuid:identifier>/",
        transactions_views.DebitCardDetails.as_view(),
        name="debit_card_transaction_detail",
    ),
    path(
        "debit-cards/payment/",
        transactions_views.CreateDebitCardTransaction.as_view(),
        name="debit_card_payment",
    ),
    # Public deposit API
    path(
        "deposits/", transactions_views.DepositList.as_view(), name="deposit_list"
    ),
    path(
        "deposits/create/",
        transactions_views.CreateDepositTransaction.as_view(),
        name="deposit_creation",
    ),
    path(
        "deposits/<uuid:identifier>/",
        transactions_views.DepositDetail.as_view(),
        name="deposit_detail",
    ),
    # Public notifications API
    path(
        "notifications/",
        notifications_views.UserNotificationList.as_view(),
        name="notification_list",
    ),
    path(
        "notifications/<type>/",
        notifications_views.UserNotificationDetailList.as_view(),
        name="notification_detail_list",
    ),
    path(
        "notifications/<type>/<int:notification_number>/",
        notifications_views.UserNotificationDetailListDetail.as_view(),
        name="notification_detail",
    ),
    path(
        "notifications/<int:notification_number>/",
        notifications_views.UserNotificationDetail.as_view(),
        name="notification_detail_single",
    ),
    # Public transactions API
    path(
        "transactions/",
        transactions_views.TransactionHistory.as_view(),
        name="transaction_history",
    ),
    path(
        "transactions/<uuid:identifier>/",
        transactions_views.TransactionDetail.as_view(),
        name="transaction_detail",
    ),
    # Public transfer API
    path(
        "transfers/",
        transactions_views.TransferHistory.as_view(),
        name="transfer_history",
    ),
    path(
        "transfers/create/",
        transactions_views.CreateTransferTransaction.as_view(),
        name="transfer_creation",
    ),
    path(
        "transfers/<uuid:identifier>/",
        transactions_views.TransferDetails.as_view(),
        name="transfer_detail",
    )
]
