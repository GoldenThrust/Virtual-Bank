from django.urls import path

from . import views
from users import views as users_views
from accounts import views as accounts_views
from credit_cards import views as credit_cards_views
from deposits import views as deposits_views
from merchants import views as merchants_views
from notifications import views as notifications_views
from payments import views as payments_views
from transactions import views as transactions_views
from transfers import views as transfers_views

app_name = 'api'

urlpatterns = [
    # path('', views, name='home'),
    path('users/', users_views.UserList.as_view(), name='users_list'),
    path('users/<int:pk>/', users_views.UserDetail.as_view(), name='users_detail'),
    path('accounts/', accounts_views.AccountList.as_view(), name='accounts_list'),
    path('accounts/<int:pk>/', accounts_views.AccountDetail.as_view(), name='accounts_detail'),
    path('credit_cards/', credit_cards_views.CreditCardList.as_view(), name='credit_cards'),
    path('credit_cards/<int:pk>/', credit_cards_views.CreditCardDetail.as_view(), name='credit_cards_detail'),
    path('deposits/', deposits_views.DepositList.as_view(), name='deposits_list'),
    path('deposits/<int:pk>/', deposits_views.DepositDetail.as_view(), name='deposits_detail'),
    path('merchants/', merchants_views.MerchantList.as_view(), name='merchants_list'),
    path('merchants/<int:pk>/', merchants_views.MerchantDetail.as_view(), name='merchants_detail'),
    path('notifications/', notifications_views.NotificationList.as_view(), name='notifications_list'),
    path('notifications/<int:pk>/', notifications_views.NotificationDetail.as_view(), name='notifications_detail'),
    path('payments/', payments_views.PaymentList.as_view(), name='payments_list'),
    path('payments/<int:pk>/', payments_views.PaymentDetail.as_view(), name='payments_detail'),
    path('transactions/', transactions_views.TransactionList.as_view(), name='transactions_list'),
    path('transactions/<int:pk>/', transactions_views.TransactionDetail.as_view(), name='transactions_detail'),
    path('transfers/', transfers_views.TransferList.as_view(), name='transfers_list'),
    path('transfers/<int:pk>/', transfers_views.TransferDetail.as_view(), name='transfers_detail'),
]