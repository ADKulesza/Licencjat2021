from django.shortcuts import render, redirect, get_object_or_404
from .forms import (ExperimentDatasetInfoForm,
                    FilesForm,
                    MetricFileForm)
from django.views.generic.edit import FormView
from .models import EEGlabDataFiles, EEGlabDataInfo
from .validator import SaveFiles, ReadMetric, ReadWordsInfo
from datetime import date
import os
from django.conf import settings
from zipfile import ZipFile
from django.http import HttpResponse
import re

from mne.externals.pymatreader.pymatreader import read_mat
from mne.utils._bunch import Bunch
import mne


def download_dataset(request):
    context = {
        'eeglab_data': EEGlabDataInfo.objects.all()
    }
    return render(request, 'files_manager/download_dataset.html', context)

def download(request, sett_id):
    eeglab_data = EEGlabDataInfo.objects.get(pk=sett_id)
    exp_path = eeglab_data.exp_path

    zipObj = ZipFile(f'{eeglab_data.name}.zip', 'w')
    for fname in os.listdir(exp_path):
        zipObj.write(os.path.join(exp_path, fname))

    zipObj.close()
    zipfile = ZipFile(f'{eeglab_data.name}.zip', 'r')
    # pobieranie
    # zip_file = open(f'{eeglab_data.name}.zip', 'r')
    response = HttpResponse(zipObj, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % f'{eeglab_data.name}.zip'
    zipfile.close()
    os.remove(f'{eeglab_data.name}.zip')

    return response



def upload_dataset_info(request):
    form = ExperimentDatasetInfoForm(request.POST or None)

    if form.is_valid():
        eeglab_dataset = form.save()

        request.session['raw_dataset_id'] = eeglab_dataset.pk
        dirname = '{}_{}_{}'.format(date.today(), eeglab_dataset.exp_type, eeglab_dataset.pk)

        exp_path = os.path.join(settings.EEGLAB_DATA_DIR, dirname)
        if not os.path.exists(exp_path):
            os.mkdir(exp_path)

        eeglab_dataset.exp_path = exp_path
        eeglab_dataset.name = dirname
        eeglab_dataset.save()
        print(eeglab_dataset)

        return redirect('upload_extra_files')

    context = {'upload_form': form
               }

    return render(request, 'files_manager/upload_dataset.html', context)



class UploadMetricInfo(FormView):
    form_class = MetricFileForm
    template_name = 'upload_dataset_files.html'  # Replace with your template.
    success_url = '/upload-dataset-files/'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        file = request.FILES.get('metric_file')
        word_metric_file = request.FILES.get('words_file')

        if form.is_valid():
            exp_id = request.session.get('raw_dataset_id')
            data = get_object_or_404(EEGlabDataInfo, pk=exp_id)
            path = os.path.join(data.exp_path, file.__str__().replace(" ", "_"))
            if os.path.exists(path):
                os.remove(path)

            data.metric = file
            if word_metric_file is not None:
                word_metric_path = os.path.join(data.exp_path,
                                                word_metric_file.__str__().replace(" ", "_"))
                if os.path.exists(word_metric_path):
                    os.remove(word_metric_path)

                data.words_metric = word_metric_file

            data.save()
            ReadMetric(path, exp_id)
            if word_metric_file is not None:
                 ReadWordsInfo(word_metric_path)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class upload_dataset_files(FormView):
    form_class = FilesForm
    template_name = 'upload_dataset_files.html'
    success_url = '/upload-check/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        dataset_id = request.session.get('raw_dataset_id')
        fv = SaveFiles(files, dataset_id)

        if form.is_valid():
            fv.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def read_tag_type(fname, uint16_codec=None):

    eeg = read_mat(fname, uint16_codec=uint16_codec)
    eeg = eeg.get('EEG', eeg)  # handle nested EEG structure
    eeg = Bunch(**eeg)
    tags_type = eeg.event['tag_type']


    return tags_type

def update_annotations(request, sett_id):
    eeglab_data = EEGlabDataInfo.objects.get(pk=sett_id)
    exp_path = eeglab_data.exp_path


    for fname in os.listdir(exp_path):
        data_path = os.path.join(exp_path, fname)
        raw = mne.io.read_raw_eeglab(data_path, preload=True)
        tags = read_tag_type(data_path, 'utf-8')

        # dodaj do bazy danych jeśli nie ma

    # return response


def upload_view(request):
    # fv = request.session.get('files')
    dataset_id = request.session.get('raw_dataset_id')
    files = EEGlabDataFiles.objects.filter(experiment=dataset_id)
    context = {
        'fdt_files': [re.search('(.*)\/(.*)$', f.file_fdt.name).group(2) for f in files],
        'set_files': [re.search('(.*)\/(.*)$', f.file_set.name).group(2) for f in files],
        'files': files
    }
    return render(request, 'files_manager/upload_view.html', context)
    pass
