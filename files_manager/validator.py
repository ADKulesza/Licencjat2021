import os
import re
import numpy as np
import pandas as pd
from django.shortcuts import get_object_or_404

from .models import EEGlabDataInfo, EEGlabDataFiles, ExperimentSubject, Words


class SaveFiles:
    def __init__(self, files, exp_id):
        self._files = files
        self.fdt_files = []
        self.set_files = []
        self.rejected_files = []
        self._exp_id = exp_id
        self._read_data()
        self.data_info = get_object_or_404(EEGlabDataInfo, pk=self._exp_id)

    def _validate_files_list(self):
        fdt_list = np.sort([fname.__str__()[:-4] for fname in self.fdt_files])
        set_list = np.sort([fname.__str__()[:-4] for fname in self.set_files])

        if len(fdt_list) != len(set_list):
            return None

        else:
            self.fdt_files = [f for _, f in sorted(zip(fdt_list, self.fdt_files))]
            self.set_files = [f for _, f in sorted(zip(set_list, self.set_files))]

    def _read_data(self):
        for file in self._files:
            file_str = file.__str__()
            if file_str.endswith('.fdt'):
                self.fdt_files.append(file)
            elif file_str.endswith('.set'):
                self.set_files.append(file)
        self._validate_files_list()

    def save(self):
        for fdt_file, set_file in zip(self.fdt_files, self.set_files):
            path = self.data_info.exp_path
            if not os.path.exists(os.path.join(path, fdt_file.__str__())) \
                    and not os.path.exists(os.path.join(path, set_file.__str__())):
                self._save_file(fdt_file, set_file)

    def _save_file(self, fdt_file, set_file):
        dataset = EEGlabDataFiles()

        dataset.file_fdt = fdt_file
        dataset.file_set = set_file
        dataset.experiment = self.data_info
        # Dodać łączenie z id z metryczką

        file_numb = re.search('[0-9]+', fdt_file.name)
        print(file_numb)
        if file_numb:
            file_number = int(file_numb.group(0))
            subject = ExperimentSubject.objects.filter(experiment=self._exp_id, name=file_number)
            if len(subject) > 0:
                subject = subject[0]

                dataset.subject = subject
        # self._data_info = get_object_or_404(ExperimentSubject, experiment=self._exp_id, name=name)
        dataset.save()
        return dataset


class ReadMetric(object):
    def __init__(self, metric_path, exp_id):
        self._path = metric_path
        self._exp_id = exp_id
        self._key_words = {'name': ['osoba badana', 'all'],
                           'age': ['wiek', 'age'],
                           'gender': ['płeć', 'plec', 'gender', 'sex']}
        self._db_dict = {}
        self._data_info = get_object_or_404(EEGlabDataInfo, pk=self._exp_id)
        self._read()

    def _read(self):

        dfs = pd.read_excel(self._path)
        nan_value = float("NaN")

        dfs.replace("", nan_value, inplace=True)

        dfs.dropna(subset=[dfs.columns[0]], inplace=True)
        for col in dfs.columns:
            for key, values in self._key_words.items():
                if col.lower() in values:
                    self._db_dict[key] = list(dfs[col])

        if 'gender' not in self._db_dict.keys():
            self._db_dict['gender'] = []
            for name in self._db_dict['name']:
                self._db_dict['gender'].append(name[0])
                # tu żeby były same liczby?

        if 'K' in self._db_dict['gender']:
            self._db_dict['gender'] = ['F' if x == 'K' else x for x in self._db_dict['gender']]

        for name, gender, age in zip(self._db_dict['name'],
                                     self._db_dict['gender'],
                                     self._db_dict['age']):
            self._update_database(name, gender, age)

    def _update_database(self, name, gender, age):
        data = ExperimentSubject()
        data.experiment = self._data_info
        data.name = name
        data.gender = gender
        data.age = age
        data.save()


class ReadWordsInfo(object):
    def __init__(self, metric_path):
        self._path = metric_path
        self._key_words = {'word': ['polish word', 'word', 'words', 'unnamed: 0',
                                    'var00001'],
                           'valence_lvl': ['valence level', 'valence_cat'],
                           'origin_lvl': ['origin level', 'origin_cat'],
                           'valence': ['valence m', 'val_m'],
                           'origin': ['origin m', 'origin_m'],
                           'arousal': ['arousal m', 'arousal_m'],
                           'concreteness': ['concreteness m', 'conc_m'],
                           'appearance_frequency': ['freqeuncy of appearance [51]', 'freq']}
        self._db_dict = {}
        # self._data_info = get_object_or_404(EEGlabDataInfo, pk=self._exp_id)
        self._read()

    def _read(self):

        dfs = pd.read_excel(self._path)

        nan_value = float("NaN")
        dfs.replace("", nan_value, inplace=True)
        dfs.dropna(subset=[dfs.columns[0]], inplace=True)

        for col in dfs.columns:
            print(col)
            for key, values in self._key_words.items():
                if col.lower() in values:
                    self._db_dict[key] = list(dfs[col])

        for word, val_lvl, orig_lvl, val, orig, aro, conc, freq in zip(self._db_dict['word'],
                                                                       self._db_dict['valence_lvl'],
                                                                       self._db_dict['origin_lvl'],
                                                                       self._db_dict['valence'],
                                                                       self._db_dict['origin'],
                                                                       self._db_dict['arousal'],
                                                                       self._db_dict['concreteness'],
                                                                       self._db_dict['appearance_frequency']):
            self._update_database(word, val_lvl, orig_lvl, val, orig, aro, conc, freq)

    def _update_database(self, word, val_lvl, orig_lvl, val, orig, aro, conc, freq):

        if not Words.objects.filter(word=word).exists():
            word_data = Words()
            word_data.word = word
            word_data.valence_lvl = val_lvl
            word_data.origin_lvl = orig_lvl
            word_data.valence = val
            word_data.origin = orig
            word_data.arousal = aro
            word_data.concreteness = conc
            word_data.appearance_frequency = freq

            word_data.save()
