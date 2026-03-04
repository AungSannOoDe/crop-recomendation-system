from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    # FIX: Changed _str_ to __str__ (double underscores)
    def __str__(self):
        return self.user.username

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    N = models.FloatField()
    P = models.FloatField()
    K = models.FloatField()
    # TIP: Fixed 'temperture' to 'temperature' and 'humiity' to 'humidity' 
    # to avoid confusion in your views later.
    temperature = models.FloatField()
    humidity = models.FloatField()
    hp = models.FloatField() # Likely meant 'ph'?
    rainfall = models.FloatField()
    predicted_label = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # FIX: Changed 'redering' to 'ordering'
        ordering = ['-created_at']
        
    # FIX: Changed _str_ to __str__ AND fixed the user attribute error
    def __str__(self):
        # 'predicted_label' is on this model, not the User model
        return f"{self.user.username} -> {self.predicted_label}"
        