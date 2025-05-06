from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(
        template_name='accounts/login.html', 
        redirect_authenticated_user=True
        ), name='default'),
    path('login/', LoginView.as_view(
        template_name='accounts/login.html', 
        redirect_authenticated_user=True
        ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]