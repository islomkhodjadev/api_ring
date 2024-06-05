from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


def validate_uzbek_phone_number(value):
    
    cleaned_number = ''.join(filter(str.isdigit, value))

    if len(cleaned_number) != 12:
        raise ValidationError("Uzbek phone numbers must be 9 digits long")

    if not cleaned_number.startswith('998'):
        raise ValidationError("Uzbek phone numbers must start with '998'")


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    founder = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=13, validators=[validate_uzbek_phone_number])
    companyName = models.CharField(max_length=200, unique=True)


class Assistant(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    content = models.TextField()
    name = models.CharField(max_length=200, unique=True)














