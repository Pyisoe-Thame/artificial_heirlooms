# accounts/urls.py

from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),

    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # removed to add a custom login view to prevent authenticated user accessing the login page
    
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),  # for login with google
]

