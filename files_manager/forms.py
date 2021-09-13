from django import forms
from .models import EEGlabDataInfo, EEGlabDataFiles


class ExperimentDatasetInfoForm(forms.ModelForm):
    class Meta:
        model = EEGlabDataInfo
        fields = ['exp_type', 'channels_system', 'number_of_participants']

class MetricFileForm(forms.Form):

    metric_file = forms.FileField(widget=forms.ClearableFileInput())
    words_file = forms.FileField(widget=forms.ClearableFileInput(), required=False)

class FilesForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
#(widget=forms.ClearableFileInput(attrs={'multiple': True}))

