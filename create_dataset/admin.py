from django.contrib import admin
from .models import UserDatasetSettings, UserDatasetFilter


class UserDatasetSettingsAdmin(admin.ModelAdmin):
    pass

class UserDatasetFilterAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserDatasetSettings, UserDatasetSettingsAdmin)
admin.site.register(UserDatasetFilter, UserDatasetFilterAdmin)

