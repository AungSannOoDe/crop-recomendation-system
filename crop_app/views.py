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
 if request.method == "POST":
    # Ensure these names match your HTML input 'name' attributes
    username = request.POST.get("email") 
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)
        
    if user is not None:
        login(request, user)
        return redirect("prediction") 
    else:
        messages.error(request, "Invalid email or password")
        # After an error, it will fall through to the final return render

 return render(request, "login.html") # This must be inside the function

from .ml.loader import predict_one,load_bundle
from django.contrib.auth.decorators import login_required
@login_required
def predict(request):
    feature_order=load_bundle()["feature_cols"]
    result=None
    last_data=None
    label = None 
    if request.method=="POST":
        data={}
        try:
            for  c in feature_order:
                data[c] = float(request.POST.get(c))


        except ValueError:
            messages.error(request,"Please enter valid numeric values")  
            return redirect("predict")  

        label = predict_one(data, top_n=3)  # returns a list
        result = label  # keep as list for template
        last_data = data

    # Store as string in database if needed
        Prediction.objects.create(
           user=request.user,
           predicted_label=", ".join(label),  # store as readable string
            **data
         )

    if isinstance(label, (list, tuple)):
          messages.success(request, f"Recommended Crops: {', '.join(label)}")
    else:
        print(request, f"Recommended Crops: {label}")
         

 
    return render(request,"predict.html",locals())
def logout_view(request):
    logout(request)
    messages.success("user logout successfully")
    return redirect("login")    
 
def signup(request):
 if request.method == "POST":
    name = request.POST.get("name")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")

    # Validation
    if not name or not email or not password:
        messages.error(request, "Please fill all required fields.")
        return redirect("signup")

    if len(password) < 6:
        messages.error(request, "Password should be at least 6 characters.")
        return redirect("signup")

    if password != confirm_password:
        messages.error(request, "Passwords do not match.")
        return redirect("signup")

    if User.objects.filter(username=name).exists():
        messages.error(request, "This username is already taken.")
        return redirect("signup")

    if User.objects.filter(email=email).exists():
        messages.error(request, "This email is already registered.")
        return redirect("signup")

    try:
        # Create auth user
        user = User.objects.create_user(
            username=name,
            email=email,
            password=password
        )

        # Create profile
        UserProfile.objects.create(
            user=user,
            phone=phone
        )

        auth_login(request, user)
        messages.success(request, f"Welcome {name}! Account created successfully.")
        return redirect("prediction")

    except Exception as e:
        print(e)  # shows real error in terminal
        messages.error(request, "An error occurred during registration.")
        return redirect("signup")

 return render(request, "signup.html")

@login_required
def user_history_view(request):
    predictions= Prediction.objects.filter(user=request.user)
    return render(request,"history.html",locals()) 
   
from django.shortcuts import get_object_or_404
@login_required
def user_delete_prediction(request,id):
    prediction= get_object_or_404(Prediction,id=id,user=request.user)
    prediction.delete()
    messages.success(request,"Entry Deleted successfully")
    return redirect('user_history')
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile    


@login_required
def profile_view(request):
    # Use get_or_create to ensure the app doesn't crash if a profile is missing
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # 1. Get data from the form
        new_name = request.POST.get("name")
        new_email = request.POST.get("email")
        new_phone = request.POST.get("phone")

        # 2. Update the User model (Auth)
        user = request.user
        user.username = new_name
        user.email = new_email
        user.save()

        # 3. Update the UserProfile model
        profile.phone = new_phone
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile') # Refresh the page to show new data

    return render(request, "profile.html", locals())

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password_view(request):
    if request.method == 'POST':
        # This form automatically requires: Old, New, and Confirm
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Important: updates the session so the user isn't logged out
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile_view')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'change-password.html', {'form': form})