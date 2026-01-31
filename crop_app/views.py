from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .models import UserProfile
# Create your views here.
def home(request):
    return render(request,"home.html")

def login_view(request):
    return  render(request,"login.html")
def predict(request):
    return render(request,"predict.html")
def logout_view(request):
    logout(request)
    messages.success("user logout successfully")
    return redirect("login")    
def signup(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        if not name or not email or not password:
            messages.error(request,"please fill required fields")
            return redirect("signup")
        if len(password) <6:
           messages.error(request,"password should be at least 6  characters")
           return redirect("signup") 
        if password != confirm_password:
           messages.error(request, "Passwords do not match.")
           return redirect("signup")
        if User.objects.filter(email=email).exists():
           messages.error(request,"This email is already registered.")
           return redirect("signup")  
        try:
           user=User.objects.create_user(
            username=name,
            email=email,
            password=password
           )  
           user.save()
           UserProfile.objects.create(user=user,email=email)
           auth_login(request,user)
           messages.success(request, "Account created! Please login.")
           return redirect("prediction")
        except Exception as e:
          messages.error(request, "An error occurred. Please try again.")   
          return redirect("signup") 

    return render(request,"signup.html")    