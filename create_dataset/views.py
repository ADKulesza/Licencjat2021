from django.shortcuts import render, redirect, get_object_or_404

from .forms import (UserDatasetSettingsStartForm,
                    UserDatasetSettingsForm,
                    DatasetSettingsEventsForm,
                    DatasetSettingsFilterForm,
                    DatasetSettingsConfirmForm)
from .models import UserDatasetSettings, UserDatasetFilter
from files_manager.models import EEGlabDataInfo, ExperimentSubject, EEGlabDataFiles, Words
from django.contrib import messages
import mne
from mne.externals.pymatreader.pymatreader import read_mat
from mne.utils._bunch import Bunch
from django.forms.models import model_to_dict
import os
import pandas as pd
import numpy as np
from .build_dataset import BuildSet
from django.http import HttpResponse


def create_dataset(request):
    start_form = UserDatasetSettingsStartForm(request.POST or None)
    exp_form = UserDatasetSettingsForm(request.POST or None)
    context = {
        'start_form': start_form,
        'form1': exp_form
    }

    if start_form.is_valid() and exp_form.is_valid():
        exp_sett = exp_form.save(commit=False)
        new_dataset = start_form.save(commit=False)
        new_dataset.user = request.user
        new_dataset.age1 = exp_sett.age1
        new_dataset.age2 = exp_sett.age2
        new_dataset.gender = exp_sett.gender
        new_dataset.exp_date1 = exp_sett.exp_date1
        new_dataset.exp_date2 = exp_sett.exp_date2
        new_dataset.save()

        request.session['dataset_id'] = new_dataset.pk

        return redirect('create-dataset-page1')

    return render(request, 'create_dataset/start_create_dataset.html', context)


def create_dataset_page1(request):
    dataset_id = request.session.get('dataset_id')
    dataset = get_object_or_404(UserDatasetSettings, pk=dataset_id)
    event_form = DatasetSettingsEventsForm(request.POST or None, instance=dataset)

    words_list = Words.objects.all()

    ch_list = ['O1', 'O2', 'T5', 'P3', 'Pz', 'P4', 'T6', 'T3',
               'C3', 'Cz', 'C4', 'T4', 'F7', 'F3', 'Fz', 'F4',
               'F8', 'Fp1', 'Fp2']
    context = {
        'event_form': event_form,
        'cat_list': ['valence_neg', 'valence_neu', 'valence_pos',
                     'origin_auto', 'origin_mix', 'origin_ref', 'pseudo_words'],
        'channel_list': ch_list,
        'words_list': words_list
    }
    if event_form.is_valid():
        dataset = event_form.save(commit=False)
        ch_list_request = request.POST.get('ch_list')
        print(len(ch_list_request))
        if len(ch_list_request) < 1:
            dataset.channels_list = ','.join(ch_list)
        else:
            dataset.channels_list = ch_list_request

        cat_selector = request.POST.get('cat_selector')
        words_selector = request.POST.get('words_selector')
        if cat_selector:
            dataset.words_cat = cat_selector
            dataset.words_list = None
        else:
            if words_selector:
                dataset.words_list = words_selector
                dataset.words_cat = None
            else:
                dataset.words_cat = 'all'
                dataset.words_list = None

        dataset.save()

        return redirect('create-dataset-page2')

    # else:
    #     messages.error(request, 'Zaznacz conajmniej jeden kanał')

    return render(request, 'create_dataset/create_dataset_page1.html',
                  context)


def create_dataset_page2(request):
    dataset_id = request.session.get('dataset_id')
    filter_form = DatasetSettingsFilterForm(request.POST or None)

    context = {
        'filter_form': filter_form,
    }

    if filter_form.is_valid():
        new_dataset = filter_form.save(commit=False)
        new_dataset.sett = get_object_or_404(UserDatasetSettings, pk=dataset_id)
        new_dataset.save()

        if request.POST.get('filter_submit') == "more":
            return render(request, 'create_dataset/create_dataset_page2.html', context)
        else:
            return redirect('confirm_dataset')

    return render(request, 'create_dataset/create_dataset_page2.html', context)


def create_dataset_page3(request):
    dataset_id = request.session.get('dataset_id')
    dataset = get_object_or_404(UserDatasetSettings, pk=dataset_id)
    confirm_form = DatasetSettingsConfirmForm(request.POST or None, instance=dataset)

    context = {
        'filter_form': confirm_form,
    }

    if confirm_form.is_valid():
        new_dataset = confirm_form.save(commit=False)
        new_dataset.sett = get_object_or_404(UserDatasetSettings, pk=dataset_id)
        new_dataset.save()

        if request.POST.get('filter_submit') == "more":
            return redirect('confirm_dataset')

    return render(request, 'create_dataset/create_dataset_page3.html', context)


def confirm_dataset(request):
    dataset_id = request.session.get('dataset_id')
    settings = UserDatasetSettings.objects.filter(pk=dataset_id)[0].__dict__
    for key, val in settings.items():
        if settings[key] is None:
            settings[key] = ''

    if len(settings['words_list']) > 0:
        settings['words_cat'] = ['Specific words']
    else:
        settings['words_cat'] = settings['words_cat'].split(',')

    if len(settings['channels_list']) >= 58:
        settings['channels_list'] = 'all'

    filters = UserDatasetFilter.objects.filter(sett_id=dataset_id)

    context = {
        'settings': settings,
        'filters': filters
    }
    print(context)

    return render(request, 'create_dataset/confirm_dataset.html', context)





def build_dataset_view(request, sett_id):
    dataset = BuildSet(sett_id)
    fname = dataset.build_set()
    if fname is None:
        pass #redirect
    pickle_file = open(fname, "r+b")

    response = HttpResponse(pickle_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % fname
    pickle_file.close()
    os.remove(fname)

    return response


    return redirect('profile')
# Na koniec podsumowanie i pytanie, zapisz, usuń, wykonaj. Potem widok -> być może z jakimś paskiem
# i cała logika przetwarzania sygnału
