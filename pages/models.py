from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

CATEGORY_CHOICES = (
    ('BIO', 'Biología'),
    ('CAL', 'Cálculo'),
    ('CIE', 'Ciencias'),
    ('NOV', 'Novedades'),
    ('OTR', 'Otros'),
)


class Page(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=250)
    content = RichTextField()
    image = models.ImageField(upload_to='pages/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    rating_total = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)

    category = models.CharField(
        max_length=3,
        choices=CATEGORY_CHOICES,
        default='OTR', 
        verbose_name="Categoría"
    )

    @property
    def average_rating(self):
        if self.rating_count:
            return round(self.rating_total / self.rating_count, 1)
        return None

    def __str__(self):
        return self.title

class Comment(models.Model):
    page = models.ForeignKey(Page, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.user.username} en {self.page.title}"
    
