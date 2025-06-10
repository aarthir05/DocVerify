from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class UploadedDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    fraud_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], default=0.0)
    verdict = models.CharField(max_length=20, default='Pending')
