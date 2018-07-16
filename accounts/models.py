from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
import os
from django.conf import settings

class Employee(AbstractUser):
    pass
