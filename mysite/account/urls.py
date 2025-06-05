from django.urls import path # type: ignore
from . import views 
from django.contrib.auth import views as auth_view # type: ignore

urlpatterns = [
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('login_user/', views.login_user, name='login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout_user/', views.logout_user, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('user_dashboard/', views.user_dashboard, name='user-dashboard'),
    path('user_dashboard_edit/<int:pk>/', views.user_dashboard_edit, name='user-dashboard-edit'),
    path('user_post_delete/<int:pk>/', views.user_post_delete, name='user-post-delete'),
]
