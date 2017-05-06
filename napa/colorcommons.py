import pandas as pd
import re
import hashlib
import random
import seaborn as sb
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import json

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
        self.data['SentDateTime'] = pd.to_datetime(self.data.SentDate)
        self.data.index = pd.to_datetime(self.data.SentDate)
        self.data.index.tz_localize('UTC').tz_convert('US/Eastern')

        if hash_id_table == None:
            self.hash_id_table = 'data/names1880.txt'


    def count_unique(self, x):
        return len(set(x))


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

    def to_sunburst(self, outPath, grp='From'):
        grouped = self.data.groupby(grp)

        parent_json = {}
        parent_json["name"] = grp
        parent_json["children"] = []

        for name, group in grouped:
            child_json = {}
            child_json["name"] = name.strftime("%Y%m%d")
            for in group.Body.value_counts()
            child_json["children"] = group.Body.value_counts()

        print('Sunburst data written to {}'.format(outPath))


    def heatmap(self, ptype='all'):

        if ptype == 'all':
            self.weekday_heatmap(len)

        else:
            if ptype == 'unique':
                self.weekday_heatmap(self.count_unique)
            else:
                print('{} is not a valid plot type'.format(ptype))


    def hash_field(self):
        baby_names_df = pd.read_csv(self.hash_id_table, names = ['baby_name', 'gender', 'ct'])
        hashed_id = [self.cute_hash(x, baby_names_df) for x in self.data.From]
        self.data.From = hashed_id


    def save_data(self, save_path):
        self.data.to_csv(save_path)


    def summary(self):
        summary_dict = {}

        # Total messages
        summary_dict['total_msg'] = len(self.data)

        # unique user count
        summary_dict['unique_users'] = len(set(self.data.From))

        summary_dict['repeat_users'] = sum(self.data.From.value_counts() > 1)

        summary_dict['dedicated_users'] = sum(self.data.From.value_counts() > 10)

        summary_dict['top_colors'] = self.data.Body.str.lower().value_counts().head(5).to_json()

        summary_dict['secret_texts'] = sum(self.data.Body.str.lower() == 'secret')
        return summary_dict


    def weekday_heatmap(self, _aggfunc):
        # Use pandas pivot table to sum up counts by weekday and hour
        # This creates a 2D dataframe containing the counts

        plot_df = self.data

        plot_df['hour'] = plot_df.SentDateTime.dt.hour
        plot_df['weekday'] = plot_df.SentDateTime.dt.weekday_name


        weekday_hour = pd.pivot_table(plot_df, values='From', index=['hour'], columns=['weekday'], aggfunc=_aggfunc, fill_value=0)
    
        # Overwrite column names with abbrev
        weekday_hour.columns = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
        # Create a heat plot with our 2D dataframe
        sb.heatmap(weekday_hour)
        plt.show()
