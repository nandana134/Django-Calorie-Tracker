from django.apps import AppConfig # type: ignore


class MyappConfig(AppConfig):
    name = 'myapp'

def ready(self):
    import myapp.signals
