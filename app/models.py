from django.db import models

# Create your models here.
class Post(models.Model):
    body = models.CharField(max_length=200)
    author = models.CharField(max_length=20)
    def __str__(self):
        return (self.body, self.author)