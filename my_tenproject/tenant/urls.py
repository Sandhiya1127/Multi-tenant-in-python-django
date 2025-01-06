# tenant/urls.py
# from django.urls import path
# from .views import register, login_view, home

# urlpatterns = [
#     path('register/', register, name='register'),
#     path('login/', login_view, name='login'),
#     path('home/', home, name='home'),
# ]

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, home

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', home, name='home'),
]

# from django.urls import path
# from django.contrib.auth import views as auth_views
# from .views import register, home

# urlpatterns = [
#     path('register/', register, name='register'),
#     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
#     path('home/', home, name='home'),
# ]