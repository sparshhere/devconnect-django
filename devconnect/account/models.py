from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True
    )

    bio = models.TextField(blank=True)

    github = models.URLField(blank=True)

    skills = models.CharField(
        max_length=250,
        blank=True
    )

    def __str__(self):
        return f'Profile of {self.user.username}'
    
class Contact(models.Model):

    user_from = models.ForeignKey(
        User,
        related_name='rel_from_set',
        on_delete=models.CASCADE
    )

    user_to = models.ForeignKey(
        User,
        related_name='rel_to_set',
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        indexes = [
            models.Index(
                fields=['-created']
            ),
        ]

        ordering = ['-created']

        unique_together = [
            'user_from',
            'user_to'
        ]

    def __str__(self):

        return f'{self.user_from} follows {self.user_to}'
    
User.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through=Contact,
        related_name='followers',
        symmetrical=False
    )
)