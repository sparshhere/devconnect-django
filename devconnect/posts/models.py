from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class PublishedManager(models.Manager):

    def get_queryset(self):

        return super().get_queryset()\
            .filter(status='published')


class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    title = models.CharField(max_length=250)

    slug = models.SlugField(max_length=250)

    body = RichTextField()

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    publish = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    tags = TaggableManager()
    users_like = models.ManyToManyField(
    User,
    related_name='posts_liked',
    blank=True
)

    objects = models.Manager()

    published = PublishedManager()

    class Meta:

        ordering = ['-publish']

        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):

        return self.title

    def get_absolute_url(self):

        return reverse(
            'post_detail',
            args=[self.id]
        )
    
class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    name = models.CharField(max_length=80)

    email = models.EmailField()

    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)

    class Meta:

        ordering = ['created']

        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):

        return f'Comment by {self.name}'