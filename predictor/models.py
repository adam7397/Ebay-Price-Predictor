from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=50)
    categoryId = models.PositiveIntegerField(default=175673, unique=True)

    def __str__(self):
        return f"{self.name}"

class saved(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    term = models.CharField(max_length=100)
    category = models.ForeignKey(category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.term}"

class recent(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    term = models.CharField(max_length=100)
    category = models.ForeignKey(category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.term}"