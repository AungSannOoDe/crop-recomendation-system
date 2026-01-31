from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login',login_view,name="login"),
    path('signup/',signup,name="signup"),
    path('predict',predict,name="prediction"),
    path('logout',logout,name='logout')
    # You can add your prediction path here later
    # path('predict/', views.predict, name='predict'),
]