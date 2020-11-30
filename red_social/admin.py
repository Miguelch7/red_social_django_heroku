from django.contrib import admin
from red_social.models import Profile, Post, Relationship, Like, Comment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Relationship)
admin.site.register(Like)
admin.site.register(Comment)
