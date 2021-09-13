from django.db import models
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings


def get_metric_path(instance, filename):
    exp_info = instance
    print(os.path.join(settings.EEGLAB_DATA_DIR,
                        exp_info.exp_path, filename))
    return os.path.join(settings.EEGLAB_DATA_DIR,
                        exp_info.exp_path, filename)

class EEGlabDataInfo(models.Model):
    EXPERIMENT_TYPE = (
        ('LDT', 'Lexical Decision Task'),
        ('ETD', 'Emotional Decision Task'),
        ('EST', 'Emotional Stroop Task'),
        ('modEST', 'Modified Emotional Stroop Task'),
    )

    CHANNELS_SYSTEMS = (
        ('10-20', '10-20'),
        ('8_opc', '8 electrodes; occipital-parietal-central'),
    )

    name = models.CharField(max_length=50)
    exp_type = models.CharField(max_length=50, choices=EXPERIMENT_TYPE)
    channels_system = models.CharField(max_length=10, choices=CHANNELS_SYSTEMS, default='10-20')
    number_of_participants = models.IntegerField(default=36)
    models.CharField(max_length=100)
    exp_path = models.CharField(max_length=100)
    metric = models.FileField(storage=FileSystemStorage(location=settings.EEGLAB_DATA_DIR,
                                                          base_url=settings.EEGLAB_DATA_URL),
                              upload_to=get_metric_path, null=True, max_length=500)
    words_metric = models.FileField(storage=FileSystemStorage(location=settings.EEGLAB_DATA_DIR,
                                                        base_url=settings.EEGLAB_DATA_URL),
                              upload_to=get_metric_path, null=True, max_length=500)
    valid = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'EEGLAB data info'



def get_upload_path(instance, filename):
    exp_info = instance.experiment
    return os.path.join(settings.EEGLAB_DATA_DIR,
                        exp_info.exp_path, filename)


class ExperimentSubject(models.Model):
    name = models.CharField(max_length=50)
    experiment = models.ForeignKey(EEGlabDataInfo, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=2)



class EEGlabDataFiles(models.Model):
    id = models.AutoField(primary_key=True)
    # name = models.CharField(max_length=50)
    subject = models.ForeignKey(ExperimentSubject, on_delete=models.CASCADE, null=True)
    experiment = models.ForeignKey(EEGlabDataInfo, on_delete=models.CASCADE)

    file_fdt = models.FileField(storage=FileSystemStorage(location=settings.EEGLAB_DATA_DIR,
                                                          base_url=settings.EEGLAB_DATA_URL),
                                upload_to=get_upload_path)
    file_set = models.FileField(storage=FileSystemStorage(location=settings.EEGLAB_DATA_DIR,
                                                          base_url=settings.EEGLAB_DATA_URL),
                                upload_to=get_upload_path)

    class Meta:
        verbose_name_plural = 'EEGLAB data files'


class Words(models.Model):
    word = models.CharField(max_length=50)
    valence = models.CharField(max_length=50)
    origin = models.CharField(max_length=50)
    valence_level = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    origin_level = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    arousal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    concreteness = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    appearance_frequency = models.IntegerField(null=True)


    class Meta:
        verbose_name_plural = 'Words'

    def __str__(self):
        return f'{self.word}'




# class ExperimentSubjectAnswer(models.Model):
#     subject_id = models.ForeignKey(ExperimentSubject, on_delete=models.CASCADE)
#     time_stamp = models.DecimalField(max_digits=15, decimal_places=2)
#     answer = models.CharField(max_length=50)
#     word = models.ForeignKey(Words, on_delete=models.CASCADE)

