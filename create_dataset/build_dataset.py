import mne
import pandas as pd
from mne.externals.pymatreader.pymatreader import read_mat
from mne.utils._bunch import Bunch

from files_manager.models import EEGlabDataInfo, ExperimentSubject, EEGlabDataFiles
from .models import UserDatasetSettings, UserDatasetFilter


def read_tag_type(fname, uint16_codec=None):
    eeg = read_mat(fname, uint16_codec=uint16_codec)
    eeg = eeg.get('EEG', eeg)  # handle nested EEG structure
    eeg = Bunch(**eeg)
    tags_type = eeg.event['tag_type']

    return tags_type


class DatasetParams(object):
    def __init__(self, dataset_settings):
        self.dataset_settings = dataset_settings
        self.subject_params = {}
        self.signal_params = {}

        self._read_params()

    def get_params(self):
        return self.subject_params, self.signal_params

    def _read_params(self):

        settings_dict = self.dataset_settings.__dict__
        for key, val in settings_dict.items():
            if val is None or val == '':
                continue
            else:
                self._conditional_params(key, val)

        self._check_baseline()

    def _conditional_params(self, key, value):
        float_values = ['event_tmin', 'event_tmax', 'baseline_tmin',
                        'baseline_tmax']
        string_values = ['heartbeat_artifacts', 'ocular_artifacts']

        if key == 'gender':
            self.subject_params[key] = value

        elif key == 'age1':
            self.subject_params['age__gte'] = value

        elif key == 'age2':
            self.subject_params['age__lte'] = value

        elif key in float_values:
            self.signal_params[key] = float(value)

        elif key in string_values:
            self.signal_params[key] = value

    def _check_baseline(self):
        if 'baseline_tmin' not in self.signal_params:
            self.signal_params['baseline_tmin'] = None


class EventCategories(object):

    def __init__(self, dataset_settings):
        self.words_cat = dataset_settings.words_cat.split(',')[:-1]
        self.condition_list = []

    def _select(self):
        cat_dict = {'valence_neg': 'Neg',
                    'valence_neu': 'Neu',
                    'valence_pos': 'Pos',
                    'origin_auto': 'A',
                    'origin_mix': 'O',
                    'origin_ref': 'R',
                    'pseudo_words': 'Pseudo'
                    }

        cat_val = [cat_dict.get(item, item) for item in self.words_cat if item.startswith('valence')]
        cat_ori = [cat_dict.get(item, item) for item in self.words_cat if item.startswith('origin')]
        cat_other = [cat_dict.get(item, item) for item in self.words_cat if
                     not item.startswith('origin') and not item.startswith('valence')]

        self._combine(cat_val, cat_ori, cat_other)

    def _combine(self, categories_val, categories_ori, categories_other):
        if len(categories_val) == 0:
            categories_val = ['Neg', 'Neu', 'Pos']

        if len(categories_ori) == 0:
            categories_ori = ['A', 'O', 'R']

        for origin in categories_ori:
            for valence in categories_val:
                self.condition_list.append(origin + valence)

        if categories_other:
            for other in categories_other:
                self.condition_list.append(other)

    def get_condition_string(self):
        self._select()

        cond = '('
        for item in self.condition_list:
            cond += f"({item})|"
        cond = cond[:-1]
        cond += ')'

        return cond


class BuildSet(object):
    def __init__(self, sett_id):

        self.dataset_settings = UserDatasetSettings.objects.get(pk=sett_id)

        self.params = DatasetParams(self.dataset_settings)

        self.filters = UserDatasetFilter.objects.filter(sett=self.dataset_settings)
        self.experiments = EEGlabDataInfo.objects.filter(exp_type=self.dataset_settings.exp_type)

    def _load_data(self, path):

        raw = mne.io.read_raw_eeglab(path, preload=True)
        return raw

    def _filter_raw(self, raw):
        for fltr in self.filters:
            raw.filter(l_freq=fltr.low_freq,
                       h_freq=fltr.high_freq,
                       method=fltr.method)
        return raw

    def _get_raw(self, data):
        raw = self._load_data(data)
        filtered_raw = self._filter_raw(raw)
        return filtered_raw

    def _event_filtering(self, raw, path):
        if self.dataset_settings.words_cat == 'all':
            events_from_annot, event_dict = mne.events_from_annotations(raw)

        # Looking for specific word
        elif self.dataset_settings.words_cat is None:
            events_from_annot, event_dict = mne.events_from_annotations(raw)

            event_tags = read_tag_type(path, uint16_codec=None)
            word_list = [tag['word'] for tag in event_tags]

            word_idx_list = []
            word_ctr = 0
            for word in word_list:
                if word in self.dataset_settings.words_list.split(','):
                    word_idx_list.append(word_ctr)
                    # może dorobić plik tekstowy z wybranymi słowami i indeksami
                word_ctr += 1
            events_from_annot = events_from_annot[word_idx_list, :]

        else:
            cond = EventCategories(self.dataset_settings).get_condition_string()
            events_from_annot, event_dict = mne.events_from_annotations(raw, regexp=cond)

        return events_from_annot

    def dealing_with_artifacts(self, raw, signal_params):
        if 'EKG' in raw.ch_names and signal_params['heartbeat_artifacts']=='Ignore':
            raw.rename_channels({'EKG': 'ECG'})
            if signal_params['heartbeat_artifacts'] == 'Delete Epochs':
                projs, events = mne.compute_proj_ecg(raw, ch_name='ECG', n_eeg=1,
                                                     ecg_l_freq = 1, ecg_h_freq = 30, no_proj=True)
                raw.add_proj(projs)
            else:
                projs, events = mne.compute_proj_ecg(raw, n_eeg=1, ecg_l_freq = 1, ecg_h_freq = 30, reject=None)
                for proj in projs:
                    raw.add_proj(proj, remove_existing=False)

        if 'EOG' in raw.ch_names and signal_params['ocular_artifacts']=='Ignore':
            if signal_params['heartbeat_artifacts'] == 'Delete Epochs':
                eog_projs, _ = mne.compute_proj_eog(raw, ch_name='EOG', n_eeg=1,
                                                reject=None, no_proj=True)
                raw.add_proj(eog_projs)
            else:
                projs, events = mne.compute_proj_eog(raw, n_eeg=1, reject=None)
                for proj in projs:
                    raw.add_proj(proj, remove_existing=False)

        return raw

    def _get_file_name(self, raw_prop):
        return f'{self.dataset_settings.name}_{self.dataset_settings.exp_type}_{raw_prop[0]}_{raw_prop[1]}.pkl'

    def _process(self, subject_params, signal_params):
        epochs_df = []

        for exp in self.experiments:
            subject_params['experiment'] = exp
            subjects = ExperimentSubject.objects.filter(**subject_params)

            for subject in subjects:
                data_files = EEGlabDataFiles.objects.filter(subject=subject)
                for data in data_files:
                    path = data.file_set.path
                    raw = self._get_raw(path)
                    raw = self.dealing_with_artifacts(raw, signal_params)
                    raw = raw.pick(self.dataset_settings.channels_list.split(','))
                    events_from_annot = self._event_filtering(raw, path)

                    epochs = mne.Epochs(raw, events_from_annot,
                                        tmin=signal_params['event_tmin'],
                                        tmax=signal_params['event_tmax'],
                                        baseline=(signal_params['baseline_tmin'],
                                                  signal_params['baseline_tmax']))

                    epochs_df.append(epochs.to_data_frame())
        if len(epochs_df) == 0:
            return None
        else:

            sfreq = raw.info['sfreq']
            epoch_samples = int(round((signal_params['event_tmax'] - signal_params['event_tmin']) * sfreq)) + 1
            fname = self._get_file_name([sfreq, epoch_samples])

            df = pd.concat(epochs_df, axis=0)
            df.to_pickle(fname)

            return fname

    def build_set(self):
        fname = self._process(self.params.subject_params, self.params.signal_params)
        if fname is None:
            return None

        return fname
