from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.forms import ModelForm, Textarea
from .models import UserDatasetSettings, UserDatasetFilter
from django.forms.widgets import NumberInput
from bootstrap_daterangepicker import widgets, fields


class UserDatasetSettingsStartForm(forms.ModelForm):
    class Meta:
        model = UserDatasetSettings
        fields = ['exp_type', 'name']
        labels = {
            'name': ('Name for your dataset settings'),
            'exp_type': ('Experiment type'),
        }


class UserDatasetSettingsForm(forms.ModelForm):
    class Meta:
        model = UserDatasetSettings
        fields = ['gender','exp_date1', 'exp_date2', 'age1', 'age2']

        labels = {
            'exp_date1': ('Start date range'),
            'exp_date2': ('End date range'),
        }

        widgets = {
            'exp_date1': DatePickerInput().start_of('event days'),
            'exp_date2': DatePickerInput().end_of('event days'),
            'age1': forms.HiddenInput(),
            'age2': forms.HiddenInput()
        }




class DatasetSettingsCategoriesForm(forms.ModelForm):
    class Meta:
        model = UserDatasetSettings
        fields = ['words_cat', 'words_list']



class DatasetSettingsEventsForm(forms.ModelForm):
    class Meta:
        model = UserDatasetSettings
        fields = ['event_tmin', 'event_tmax', 'channels_list', 'baseline_tmin',
                  'baseline_tmax', 'heartbeat_artifacts', 'ocular_artifacts']

        labels = {
            'heartbeat_artifacts': 'Heartbeat Artifacts',
            'ocular_artifacts': 'Ocular Artifacts'
        }

        widgets = {
            'event_tmin': forms.HiddenInput(),
            'event_tmax': forms.HiddenInput(),
            'channels_list': forms.HiddenInput(),
            'baseline_tmin': forms.HiddenInput(),
            'baseline_tmax': forms.HiddenInput(),
        }

class DatasetSettingsFilterForm(forms.ModelForm):
    class Meta:
        model = UserDatasetFilter
        fields = ['order', 'low_freq', 'high_freq', 'method']

        labels = {
            'low_freq': ('Low Frequency'),
            'high_freq': ('High Frequency'),
        }

class DatasetSettingsConfirmForm(forms.ModelForm):
    class Meta:
        model = UserDatasetSettings
        fields = ['download_file_type']




