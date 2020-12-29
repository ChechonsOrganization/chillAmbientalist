# Django modules
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
# Current-app modules
from .models import Gallery

@receiver(post_save, sender=Gallery)
def gallery_save_handler(sender, **kwargs):
    if settings.DEBUG:
        print(f"{kwargs['instance']} saved.")

@receiver(post_delete, sender=Gallery)
def gallery_delete_handler(sender, **kwargs):
    if settings.DEBUG:
        print(f"{kwargs['instance']} deleted.")
