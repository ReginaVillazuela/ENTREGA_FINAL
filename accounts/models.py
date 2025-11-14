from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Opciones de Título Académico
TITLE_CHOICES = [
    ('Estudiante', 'Estudiante'),
    ('Ingeniero', 'Ingeniero/a'),
    ('Profesor', 'Profesor/a'),
    ('Investigador', 'Investigador/a'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biografía")
    location = models.CharField(max_length=30, blank=True, verbose_name="Ubicación (Ej: UNSAM)")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    title = models.CharField(max_length=30, choices=TITLE_CHOICES, default='Estudiante', verbose_name="Título/Rol")
    
    # Campo opcional para foto de perfil
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics', blank=True, verbose_name="Foto de Perfil")

    def __str__(self):
        return f'Perfil de {self.user.username}'

# Señales para crear/actualizar el perfil automáticamente al crear/actualizar el usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()