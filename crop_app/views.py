from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
import openpyxl

# Import your models
from .models import UserProfile, Prediction 
from .ml.loader import predict_one, load_bundle
def home(request):
  total_users = User.objects.filter(is_staff=False).count()
  total_predictions = Prediction.objects.count()
    
# Optional: Count unique crops predicted across the system
# This adds a "Crops Supported" stat
  total_crops = 41 # Usually a fixed number based on your ML model
    
  return render(request, "home.html", {
    "total_users": total_users,
    "total_predictions": total_predictions,
    "total_crops": total_crops
  })

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("name") 
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            # Ensure "predict" matches your urls.py name
            return redirect("predict") 
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff or user.is_superuser:
                auth_login(request, user)
                return redirect("admin_dashboard")
            else:
                messages.error(request, "You are not authorized as admin.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "admin_login.html")

@login_required
def predict(request):
    bundle = load_bundle()
    feature_order = bundle["feature_cols"]
    result = None
    last_data = None
    label = None 

    if request.method == "POST":
        data = {}
        try:
            for c in feature_order:
                val = request.POST.get(c)
                data[c] = float(val) if val else 0.0
        except ValueError:
            messages.error(request, "Please enter valid numeric values")  
            return redirect("predict")  

        # Prediction Logic
        label = predict_one(data, top_n=3)  # Returns a list
        result = label
        last_data = data

        # Save to Database
        Prediction.objects.create(
            user=request.user,
            predicted_label=", ".join(label),
            **data
        )

        messages.success(request, f"Recommended Crops: {', '.join(label)}")
 
    return render(request, "predict.html", locals())

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("login")    

def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not name or not email or not password:
            messages.error(request, "Please fill all required fields.")
            return redirect("signup")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already taken.")
            return redirect("signup")

        try:
            user = User.objects.create_user(username=name, email=email, password=password)
            UserProfile.objects.create(user=user, phone=phone)
            auth_login(request, user)
            messages.success(request, f"Welcome {name}!")
            return redirect("predict")
        except Exception as e:
            messages.error(request, "An error occurred during registration.")
            return redirect("signup")

    return render(request, "signup.html")

@login_required
def user_history_view(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-id')
    return render(request, "history.html", locals()) 
   
@login_required
def user_delete_prediction(request, id):
    prediction = get_object_or_404(Prediction, id=id, user=request.user)
    prediction.delete()
    messages.success(request, "Entry deleted successfully")
    return redirect('user_history')

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        new_name = request.POST.get("name")
        new_email = request.POST.get("email")
        new_phone = request.POST.get("phone")

        user = request.user
        user.username = new_name
        user.email = new_email
        user.save()

        profile.phone = new_phone
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile_view')

    return render(request, "profile.html", locals())

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully!')
            return redirect('profile_view')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'change-password.html', {'form': form})

import json
from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from collections import Counter
from django.contrib.auth.decorators import user_passes_test

# Assuming your is_staff helper is defined above or imported
def is_staff(user):
    return user.is_authenticated and user.is_staff

from .models import Prediction

@user_passes_test(is_staff, login_url='admin_login')
def admin_dashboard_view(request):
    # 1. Basic Counts
    total_users = User.objects.filter(is_staff=False).count()
    total_predictions = Prediction.objects.count()

    # --- START OF FIX ---
    # 2. Individual Crop Distribution
    # We fetch all the multi-crop strings from the database
    all_prediction_strings = Prediction.objects.values_list('predicted_label', flat=True)
    
    all_individual_crops = []
    for row in all_prediction_strings:
        # Split "Rice, Jute, Maize" into ["Rice", "Jute", "Maize"]
        crops = [c.strip().title() for c in row.split(',')]
        all_individual_crops.extend(crops)
    
    # Use Counter to see which individual crop appears most often
    counts = Counter(all_individual_crops).most_common(10)
    
    # Prepare the lists for the chart
    crops_label = [item[0] for item in counts]
    crops_count = [item[1] for item in counts]
    # --- END OF FIX ---

    # 3. Weekly Trends (Keep this as is)
    today = timezone.localdate()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    day_labels = [d.strftime('%b %d') for d in days]
    day_count = [Prediction.objects.filter(created_at__date=d).count() for d in days]

    # 4. Context for Template
    context = {
        "total_users": total_users,
        "total_predictions": total_predictions, 
        "crop_labels": json.dumps(crops_label),
        "crop_count": json.dumps(crops_count),
        "day_labels": json.dumps(day_labels),
        "day_count": json.dumps(day_count),
    }

    return render(request, 'admin-dashboard.html', context)
@user_passes_test(is_staff, login_url='admin_login')
def user_list_view(request):
    # Fetch all regular users and their profiles in one query
    users = User.objects.filter(is_staff=False).select_related('userprofile').order_by('-date_joined')
    return render(request, 'users.html', {'users': users})

@user_passes_test(is_staff, login_url='admin_login')
def export_popular_crops_excel(request):
    # 1. Same logic as your dashboard to count individual crops
    all_prediction_strings = Prediction.objects.values_list('predicted_label', flat=True)
    all_individual_crops = []
    
    for row in all_prediction_strings:
        crops = [c.strip().title() for c in row.split(',')]
        all_individual_crops.extend(crops)
    
    counts = Counter(all_individual_crops).most_common()

    # 2. Create an Excel Workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Popular Crops Analysis"

    # Add Headers
    ws.append(['Crop Name', 'Total Recommendations', 'Percentage (%)'])

    # 3. Add Data Rows
    total_count = sum(c for _, c in counts)
    for crop, count in counts:
        percentage = (count / total_count * 100) if total_count > 0 else 0
        ws.append([crop, count, round(percentage, 2)])

    # 4. Prepare the Response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="popular_crops_report.xlsx"'
    
    wb.save(response)
    return response