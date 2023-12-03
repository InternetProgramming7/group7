from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Comment(models.Model):
    post=models.ForeignKey('community.Post', on_delete=models.CASCADE, related_name='comments')
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_author")
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text

class CommentDelivery(models.Model):
    post=models.ForeignKey('community.Delivery', on_delete=models.CASCADE, related_name='comments_delivery')
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_delivery")
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text

class Post(models.Model):
    CATEGORY_CHOICES=[
        ('혼밥싫어','Food'),
        ('같이 배달시켜요','Delivery'),
    ]

    title = models.CharField(max_length=30)
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='food_posts', null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    head_image = models.ImageField(upload_to='community/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='community/files/%Y/%m/%d/', blank=True)
    category=models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='food')
    community=models.CharField(max_length=20)
    def __str__(self):
        return f'[{self.pk}]{self.title}'
    def get_absolute_url(self):
        return f'/community/{self.pk}/'


class Delivery(models.Model):
    CATEGORY_CHOICES=[
        ('생필품','Daily'),
        ('OTT','OTT'),
    ]

    title = models.CharField(max_length=30)
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delivery_posts', null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    head_image = models.ImageField(upload_to='community/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='community/files/%Y/%m/%d/', blank=True)
    category_delivery=models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='daily')
    community=models.CharField(max_length=20)
    def __str__(self):
        return f'[{self.pk}]{self.title}'
    def get_absolute_url(self):
        return f'/community/{self.pk}/'
