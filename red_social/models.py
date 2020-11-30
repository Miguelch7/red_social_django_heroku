from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='media', default='default.png')

    def __str__(self):
        return f'Perfil de {self.user.username}'

    def following(self):
        user_ids = Relationship.objects.filter(from_user=self.user)\
                            .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def followers(self):
        user_ids = Relationship.objects.filter(to_user=self.user)\
                        .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    class Meta:
        ordering = ['-timestamp']

        def __str__(self):
            return f'{self.user.username}: {self.content}'

    def likes(self):
        user_ids = Like.objects.filter(to_post=self.id, type='L')\
                            .values_list('from_user', flat=True)
        return Post.objects.filter(id__in=user_ids)

    def dislikes(self):
        user_ids = Like.objects.filter(to_post=self.id, type='D')\
                            .values_list('from_user', flat=True)
        return Post.objects.filter(id__in=user_ids)

    def comments(self):
        user_ids = Comment.objects.filter(to_post=self.id)\
                            .values_list('from_user', flat=True)
        return Post.objects.filter(id__in=user_ids)


class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='relationship', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'

    class Meta:
        indexes = [
            models.Index(fields=['from_user', 'to_user',]),
        ]

class Comment(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    to_post = models.ForeignKey(Post, related_name='comment_post', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()


class Like(models.Model):
    from_user = models.ForeignKey(User, related_name='like_user', on_delete=models.CASCADE)
    to_post = models.ForeignKey(Post, related_name='like_post', on_delete=models.CASCADE)
    types = [
        ('L' ,'Like'),
        ('D' ,'Dislike')
    ]
    type = models.CharField(max_length=1, choices=types, null=True, blank=True)
