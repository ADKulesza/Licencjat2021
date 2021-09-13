from django.db import models
from django.conf import settings
from django.urls import reverse


class UserDatasetSettings(models.Model):

    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
        (None, 'All')
    )

    EXPERIMENT_TYPE = (
        ('LDT', 'Lexical Decision Task'),
        ('EST', 'Emotional Stroop Task'),
        ('modEST', 'Modified Emotional Stroop Task'),
    )

    ARTIFACTS = (
        ('ignore', 'Ignore'),
        ('delete', 'Delete Epochs'),
        ('interpolate', 'Interpolate'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    exp_type = models.CharField(max_length=50, choices=EXPERIMENT_TYPE, default='all')

    exp_date1 = models.DateTimeField(null=True, blank=True)
    exp_date2 = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    age1 = models.IntegerField(null=True, blank=True)
    age2 = models.IntegerField(null=True, blank=True)

    words_cat = models.CharField(max_length=150, default='all', null=True)
    words_list = models.CharField(max_length=1000, null=True, blank=True)

    channels_list = models.CharField(max_length=100, default='all')
    event_tmin = models.DecimalField(max_digits=3, decimal_places=2, default=-0.2)
    event_tmax = models.DecimalField(max_digits=3, decimal_places=2, default=0.5)

    baseline_tmin = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, default=None)
    baseline_tmax = models.DecimalField(max_digits=3, decimal_places=2, null=True, default=0)

    heartbeat_artifacts = models.CharField(max_length=50, choices=ARTIFACTS, default='Ignore')
    ocular_artifacts = models.CharField(max_length=50, choices=ARTIFACTS, default='Ignore')

    download_file_type = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('create-dataset-page1', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'User dataset settings'


class UserDatasetFilter(models.Model):

    # FILTERS = {
    #     ('lowpass', 'Lowpass'),
    #     ('highpass', 'Highpass'),
    #     ('bandpass', 'Bandpass'),
    #     ('bandstop', 'Bandstop')
    # }

    DIGITAL_FILTERS = {
        ('fir', 'FIR'),
        ('iir', 'IIR')
    }

    sett = models.ForeignKey(UserDatasetSettings, on_delete=models.CASCADE)
    low_freq = models.DecimalField(max_digits=4, decimal_places=2, default=None, null=True, blank=True)
    high_freq = models.DecimalField(max_digits=4, decimal_places=2, default=None, null=True, blank=True)
    # type = models.CharField(max_length=50, choices=FILTERS)
    order = models.IntegerField()

    method = models.CharField(max_length=3, choices=DIGITAL_FILTERS, default='fir')
