# apps/usermodule/urls.py
from django.urls import path
from . import views   # <- important: import views from the same app

app_name = 'users'    # optional but useful if you use namespaced URLs

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
