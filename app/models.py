from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Post(models.Model):
    # This links the post to an author.
    # If an author is deleted, all their posts are also deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The title of the post
    title = models.CharField(max_length=200)
    
    # The main content of the post
    body = models.TextField()
    # Timestamp for when the post was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # This is what shows up in the Django admin panel
        return f'"{self.title}" by {self.author.username}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username