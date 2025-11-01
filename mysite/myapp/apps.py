from django.apps import AppConfig  # type: ignore


class MyappConfig(AppConfig):
    name = 'myapp'
    verbose_name = "My App"

    def ready(self):
        # Import signals so they are registered when Django starts.
        # Keep imports inside ready() to avoid import-time DB access or circular imports.
        try:
            import myapp.signals  # noqa: F401
        except Exception as e:
            # Do not raise here; log so deploy logs show the problem.
            print("Warning: could not import myapp.signals:", e)
