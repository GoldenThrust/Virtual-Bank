from django.urls import path

from . import views
from users import views as users_views
from accounts import views as accounts_views
from credit_cards import views as credit_cards_views
from debit_cards import views as debit_cards_views
from deposits import views as deposits_views
from merchants import views as merchants_views
from notifications import views as notifications_views

# from payments import views as payments_views
from transactions import views as transactions_views
from transfers import views as transfers_views
from .views import ListApiUrls

from rest_framework_simplejwt.views import TokenVerifyView


app_name = "api"

urlpatterns = [
    path("", ListApiUrls.as_view(), name="api_overview"),
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
    path(
        "admin/debit-cards/transactions/",
        debit_cards_views.TransactionDebitCard.as_view(),
        name="admin_debit_card_transactions",
    ),
    path(
        "admin/debit-cards/transactions/<int:pk>/",
        debit_cards_views.TransactionDebitCardDetail.as_view(),
        name="admin_debit_card_transaction_detail",
    ),
    # Deposit management (admin only)
    path(
        "admin/deposits/",
        deposits_views.DepositList.as_view(),
        name="admin_deposit_list",
    ),
    path(
        "admin/deposits/<int:pk>/",
        deposits_views.DepositDetail.as_view(),
        name="admin_deposit_detail",
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
        transactions_views.TransactionList.as_view(),
        name="admin_transaction_list",
    ),
    path(
        "admin/transactions/<int:pk>/",
        transactions_views.TransactionDetail.as_view(),
        name="admin_transaction_detail",
    ),
    # Transfer management (admin only)
    path(
        "admin/transfers/",
        transfers_views.TransferList.as_view(),
        name="admin_transfer_list",
    ),
    path(
        "admin/transfers/<int:pk>/",
        transfers_views.TransferDetail.as_view(),
        name="admin_transfer_detail",
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
        "accounts/", accounts_views.UserAccountList.as_view(), name="user_account_list"
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
        name="user_debit_card_list",
    ),
    path(
        "debit-cards/<int:number>/",
        debit_cards_views.UserDebitCardDetail.as_view(),
        name="debit_card_detail",
    ),
    path(
        "debit-cards/transactions/",
        debit_cards_views.UserTransactionDebitCardList.as_view(),
        name="user_debit_card_transactions",
    ),
    path(
        "debit-cards/transactions/<uuid:identifier>/",
        debit_cards_views.UserTransactionDebitCardDetail.as_view(),
        name="debit_card_transaction_detail",
    ),
    path(
        "debit-cards/payment/",
        transactions_views.TransactionDebitCardCreate.as_view(),
        name="debit_card_payment",
    ),
    # Public deposit API
    path(
        "deposits/", deposits_views.UserDepositList.as_view(), name="user_deposit_list"
    ),
    path(
        "deposits/create/",
        transactions_views.TransactionDepositCreate.as_view(),
        name="deposit_creation",
    ),
    path(
        "deposits/<uuid:identifier>/",
        deposits_views.UserDepositDetail.as_view(),
        name="deposit_detail",
    ),
    # Public notifications API
    path(
        "notifications/",
        notifications_views.UserNotificationList.as_view(),
        name="user_notification_list",
    ),
    path(
        "notifications/<type>/",
        notifications_views.UserNotificationDetailList.as_view(),
        name="user_notification_detail_list",
    ),
    path(
        "notifications/<type>/<int:notification_number>/",
        notifications_views.UserNotificationDetailListDetail.as_view(),
        name="user_notification_detail",
    ),
    path(
        "notifications/<int:notification_number>/",
        notifications_views.UserNotificationDetail.as_view(),
        name="user_notification_detail_single",
    ),
    path(
        "notifications/<int:pk>/",
        notifications_views.UserNotificationDetail.as_view(),
        name="user_notification_detail_single",
    ),
    # Public transactions API
    path(
        "transactions/",
        transactions_views.TransactionHistory.as_view(),
        name="transaction_history",
    ),
    path(
        "transactions/<uuid:identifier>/",
        transactions_views.UserTransactionDetail.as_view(),
        name="transaction_detail",
    ),
    # Public transfer API
    path(
        "transfers/",
        transfers_views.UserTransferList.as_view(),
        name="user_transfer_list",
    ),
    path(
        "transfers/create/",
        transactions_views.TransactionTransferCreate.as_view(),
        name="transfer_creation",
    ),
    path(
        "transfers/<uuid:identifier>/",
        transfers_views.UserTransferDetails.as_view(),
        name="transfer_detail",
    ),
    # credit_cards urlpattern archives
    # path('credit_cards/', credit_cards_views.CreditCardList.as_view(), name='credit_cards'),
    # path('credit_cards/<int:pk>/', credit_cards_views.CreditCardDetail.as_view(), name='credit_cards_detail'),
    # path('credit_cards/lists/', credit_cards_views.UserCreditCardList.as_view(), name='credit_cards_list'),
    # path('credit_cards/details/<int:number>/', credit_cards_views.UserCreditCardDetail.as_view(), name='user_credit_cards_detail'),
    # path('credit_cards/create/', transactions_views.CreditCardCreate.as_view(), name='credit_cards_create'),
    # merchants urlpattern (admin only)
    # path('merchants/', merchants_views.MerchantList.as_view(), name='merchants_list'),
    # path('merchants/<int:pk>/', merchants_views.MerchantDetail.as_view(), name='merchants_detail'),
    # (public API url)
    # path('merchants/create/', merchants_views.MerchantCreate.as_view(), name='merchants_create'),
    # path('merchants/details/', merchants_views.MerchantDetails.as_view(), name='merchants_details'),
    # notifications urlpattern (admin only)
    # payments urlpattern archive
    # path('payments/', payments_views.PaymentList.as_view(), name='payments_list'),
    # path('payments/<int:pk>/', payments_views.PaymentDetail.as_view(), name='payments_detail'),
]
