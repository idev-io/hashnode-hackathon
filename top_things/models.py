from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from .utils import path_and_rename, resize_image


class User(AbstractUser):
    pass


class Category(models.Model):
    '''Category Model'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.category


class Thing(models.Model):
    '''Things Model'''

    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'

    RANK_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rank = models.CharField(max_length=12, choices=RANK_CHOICES, default=BEGINNER,)
    title = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=200)
    link = models.CharField(max_length=1000)
    picture = models.ImageField(upload_to=path_and_rename, default='things/default.jpg')
    description = RichTextField()
    slug=models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    
    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        self.picture = resize_image(self.picture, size=(926, 617))

        super().save(*args, **kwargs)


# Create slug
def create_slug(instance, new_slug=None):
    """Create slug"""

    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Thing.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug


# Turn title into slug 
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Thing)


