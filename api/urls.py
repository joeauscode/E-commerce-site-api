from . import views
from django.urls import path





urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # path('upload-avatar/', views.AvatarUploadView.as_view(), name='upload-avatar'),
    
]