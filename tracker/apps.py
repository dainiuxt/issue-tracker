from django.apps import AppConfig
# from django.db.models.signals import post_save

class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    def ready(self):
        from .signals import (create_profile,
                            save_profile)
                            