from django.db.models.signals import post_save  # signalas (būna įvairių)
from django.contrib.auth.models import User     # siuntėjas
from django.dispatch import receiver            # priėmėjas (dekoratorius)
from .models import People

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs): 
    if created:
        People.objects.create(user=instance)
        print('KWARGS: ', kwargs)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.people.save()
