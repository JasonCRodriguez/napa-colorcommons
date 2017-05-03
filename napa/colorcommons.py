import pandas as pd
import re
import hashlib
import random


class UserTexts(object):

    def __init__(self, data_file, remap_names=None, hash_id_table=None):

        df = pd.read_csv(data_file)

        # option to remap names to required columns
        if remap_names:
            for new_name, old_name in remap_names.items():
                df[new_name] = df[old_name]

        req_columns = ['From', 'Body', 'SentDate', 'Status']

        try:
            self.data = df[req_columns]

        except KeyError as er:
            raise KeyError(er,
                           'Req columns: {}'.format(', '.join(req_columns)))

        # use datetime as index
        self.data.index = pd.to_datetime(self.data.SentDate)

        if hash_id_table == None:
            self.hash_id_table = 'data/names1880.txt'

    def cute_hash(self, x, baby_names_df):

        hexhash = hashlib.md5(bytes(str(x), 'UTF8')).digest()
        suffix = ''.join([str(hexhash[2]), str(hexhash[3])])

        if hexhash[0] % 2:
            id_name = baby_names_df[baby_names_df.gender == 'F'].iloc[hexhash[1]].baby_name 
            full_id = ''.join([id_name, suffix])
        else:
            id_name = baby_names_df[baby_names_df.gender == 'M'].iloc[hexhash[1]].baby_name 
            full_id = ''.join([id_name, suffix])
        return full_id 

    def heatmap(self):
        pass

    def hash_field(self):
        baby_names_df = pd.read_csv(self.hash_id_table, names = ['baby_name', 'gender', 'ct'])
        hashed_id = [self.cute_hash(x, baby_names_df) for x in self.data.From]
        self.data.From = hashed_id

    def save_data(self, save_path):
        self.data.to_csv(save_path)

    def summary(self):
        pass

    def show_plot_options(self):
        pass
