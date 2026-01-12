from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=280)  # Wie bei Twitter/Threads
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")
    
    class Meta:
        ordering = ['-timestamp']  # the newest posts first
    
    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"
    
    def like_count(self):
        return self.likes.count()


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')  # prevents duplicate follows
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"