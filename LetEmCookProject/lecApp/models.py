
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random

def generate_code():
    return '{:06d}'.format(random.randint(0, 999999))

class EmailMFA(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def regenerate(self):
        self.code = generate_code()
        self.created_at = timezone.now()
        self.save()
