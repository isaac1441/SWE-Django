from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Post(models.Model):
    # This links the post to an author.
    # If an author is deleted, all their posts are also deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        # This is what shows up in the Django admin panel
        return f'"{self.title}" by {self.author.username}'

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='comments', 
        on_delete=models.CASCADE
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username}: "{self.body[:30]}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username