from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Meme(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='memes/')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    emoji_counts = models.JSONField(default=dict)
    public = models.BooleanField(default=True)
    retweets = models.ManyToManyField(User, related_name='retweeted_memes', through='Retweet')

    def __str__(self):
        return self.title

class Comment(models.Model):
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    emoji = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} על {self.meme.title}"

class MemeEmoji(models.Model):
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='emoji_reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=2)

    class Meta:
        unique_together = ('meme', 'user')

class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'meme')