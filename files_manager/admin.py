from django.contrib import admin
from .models import (EEGlabDataInfo,
                     EEGlabDataFiles,
                     ExperimentSubject,
                     Words)
class EEGlabDataInfoAdmin(admin.ModelAdmin):
    pass

class EEGlabDataFilesAdmin(admin.ModelAdmin):
    pass

class ExperimentSubjectAdmin(admin.ModelAdmin):
    pass

class WordsAdmin(admin.ModelAdmin):
    pass


admin.site.register(EEGlabDataInfo, EEGlabDataInfoAdmin)
admin.site.register(EEGlabDataFiles, EEGlabDataFilesAdmin)
admin.site.register(ExperimentSubject, ExperimentSubjectAdmin)
admin.site.register(Words, WordsAdmin)