from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils.text import slugify

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'P', 'Published'

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    tags = TaggableManager()  # Allows tagging of posts
    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        local_pub = timezone.localtime(self.publish) #converts utc time to local
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )

    slug = models.SlugField(max_length=250, unique_for_date='publish', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Comment(models.Model): # Model for comments on blog posts
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE, # If post is deleted, its comments are also deleted
                             related_name='comments') # Allows accessing comments from a Post object as post.comments.all()
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) # Comments can be set to inactive if moderation is needed

    class Meta:
        ordering = ['created'] # Order comments by creation date, oldest first
        indexes = [
            models.Index(fields=['created']), # Add an index for faster queries on 'created' field
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
