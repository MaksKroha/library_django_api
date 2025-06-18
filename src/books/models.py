from django.db import models

from users.models import User

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)


    def __str__(self):
        return self.name