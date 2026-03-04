from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login', login_view, name="login"),
    path('signup/', signup, name="signup"),
    
    # CHANGED: name="prediction" -> name="predict"
    # This matches return redirect("predict") in your views.py
    path('predict', predict, name="predict"), 
    
    path('logout', logout_view, name='logout'),
    path('user_history', user_history_view, name='user_history'),
    path('history_delete/<int:id>/', user_delete_prediction, name="user_delete_prediction"),
    path('profile', profile_view, name='profile'),
    path('change-password', change_password_view, name='change-password'),
    
    # CHANGED: name="admin-login" -> name="admin_login" 
    # To match your @user_passes_test(login_url='admin_login')
    path('admin-login', admin_login_view, name='admin_login'),
    
    path('admin_dashboard', admin_dashboard_view, name='admin_dashboard'),
    path('admin_dashboard/users/', user_list_view, name='admin_user_list'),
    path('admin_dashboard/export-crops/', export_popular_crops_excel, name='export_crops_excel')
]