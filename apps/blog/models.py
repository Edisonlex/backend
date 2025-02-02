from django.db import models
import uuid
from django.utils import timezone
from apps.category.models import Category
from tinymce.models import HTMLField

class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    blog_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    thumbnail = models.URLField(blank=True, null=True)  # Cambiado de ImageField a URLField
    video = models.URLField(blank=True, null=True)  # Cambiado de FileField a URLField
    description = HTMLField()
    excerpt = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    published = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=options, default='draft')

    objects = models.Manager()
    postobjects = PostObjects()

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

    def get_video(self):
        if self.video:
            return self.video  # Devuelve la URL directamente
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail  # Devuelve la URL directamente
        return ''