from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('dashboard/', login_required(views.DashBoard.as_view()), name='dashboard'),
]

 # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', login_required(auth_views.LogoutView.as_view()), name='logout'),
    # path('register/', views.register, name='register'),
    # path('profile/', login_required(views.profile), name='profile'),
    # path('profile/edit/', login_required(views.edit_profile), name='edit_profile'),
    # path('profile/change_password/', login_required(views.change_password), name='change_password'),