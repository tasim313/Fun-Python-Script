from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.core.exceptions import ImproperlyConfigured

app_models = apps.get_app_config('core').get_models()

for model in app_models:
    try:
        # Dynamically create a ModelAdmin class
        class DynamicAdmin(admin.ModelAdmin):
            list_display = [field.name for field in model._meta.fields if field.name != 'id']
            search_fields = [field.name for field in model._meta.fields if field.get_internal_type() in ('CharField', 'TextField')]
            list_filter = [field.name for field in model._meta.fields if field.get_internal_type() in ('BooleanField', 'NullBooleanField', 'DateField', 'DateTimeField', 'ForeignKey')]

        admin.site.register(model, DynamicAdmin)
    
    except (AlreadyRegistered, ImproperlyConfigured):
        pass
