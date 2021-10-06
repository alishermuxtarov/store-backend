from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'catalog'
    verbose_name = 'Каталог'

    def ready(self):
        pass
