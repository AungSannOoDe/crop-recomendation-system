from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login',login,name="login"),
    path('sign-up',signup,name="signup")
    # You can add your prediction path here later
    # path('predict/', views.predict, name='predict'),
]