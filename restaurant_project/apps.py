from django.apps import AppConfig


class RestaurantProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant_project'

    def ready(self):
        from . import signals
        signals.request_finished.connect(signals.create_profile, signals.save_profile)