# Ensure the custom AppConfig is used in older Django versions.
# If your INSTALLED_APPS already includes 'myapp.apps.MyappConfig', this is harmless.
default_app_config = 'myapp.apps.MyappConfig'
