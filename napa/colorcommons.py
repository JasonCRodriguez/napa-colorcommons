import json
import re
import hashlib
import random
from datetime import datetime
import logging
import difflib
import calendar

import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class UserTexts(object):

    def __init__(self, data_file, remap_names=None, hash_id_table=None):

        logging.basicConfig()

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

        # cleanup body text
        self.data['Body'] = self.data.Body.str.lower().replace(r"\s+", "", regex=True)

        if hash_id_table == None:
            self.hash_id_table = 'data/names1880.txt'

        self.has_hash = False


    def check_hash(f):

        def wrapper(*args, **kwargs):
            if args[0].has_hash:
                return f(*args, **kwargs)

            else:
                logging.warning('not sure if the data set has a hashed id. Confirm then set has_hash = True') 

        return wrapper


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


    def to_date_sunburst(self, outfile, min_count = 5):

        # Create month and day variables
        self.data['Month'] = self.data.SentDateTime.dt.\
                             month.apply(lambda x: calendar.month_abbr[x])
        self.data['Day'] = self.data.SentDateTime.dt.day

        label = 'Dates'

            
        mon_grouped = self.data.groupby('Month')
        root_dict = {}
        root_dict['name'] = label
        root_dict['children'] = []
    
        # iterate through each month
        for month, group in mon_grouped:
            
            month_dict = {}
            day_list = []

            day_grouped = group.groupby('Day')

            for day, day_group in day_grouped:

                day_dict = {}
                color_list = []

                for (color, count) in day_group.Body.value_counts().to_dict().items():
                    if count < min_count:
                        continue
    
                    color_list.append({
                                      'name': str(color)
                                      ,'size': int(count)
                                      ,'color': self.translate_color(color)
                                     })
                # Add day and colors to day dictionary
                day_dict['name'] = str(day)
                day_dict['children'] = color_list

                # Append day to day_list
                day_list.append(day_dict)

            # Create month dict
            month_dict['name'] = str(month)
            month_dict['children'] = day_list
            root_dict['children'].append(month_dict)
            
    
        with open(outfile, 'w') as f:
            f.write(json.dumps(root_dict, indent = 4, ensure_ascii=False))
        print('Date Sunburst data written to {}'.format(outfile))
        
        return root_dict


    @check_hash
    def to_user_sunburst(self, outfile, min_count = 5):
        # function that creates a json file for the user sunburst plot

        label = 'Users'

        grp = 'From'
            
        grouped = self.data.groupby(grp)
        root_dict = {}
        root_dict['name'] = label
        root_dict['children'] = []
    
        for user, group in grouped:
        # iterate through each user (eg name)
            
            user_dict = {}
            color_list = []
               
            for (color, count) in group.Body.value_counts().to_dict().items():
            # iterate through each color text message

            # Only keep texts that occur a minimum of min_count
                if count < min_count:
                    continue
    
            # Append a dict with the color, the count, and rgb values
                color_list.append({
                                  'name': str(color)
                                  ,'size': int(count)
                                  ,'color': self.translate_color(color)
                                  })
            
            # Create a dict with two key value pairs    
            user_dict['name'] = str(user)
            user_dict['children'] = color_list
                
            root_dict['children'].append(user_dict)

    
        with open(outfile, 'w') as f:
            f.write(json.dumps(root_dict, indent = 4, ensure_ascii=False))
        print('User Sunburst data written to {}'.format(outfile))
        
        return root_dict


    def hash_id(self):
        baby_names_df = pd.read_csv(self.hash_id_table, names = ['baby_name', 'gender', 'ct'])
        hashed_id = [self.cute_hash(x, baby_names_df) for x in self.data.From]
        self.data.From = hashed_id

        self.has_hash = True


    def heatmap(self, ptype='all'):

        if ptype == 'all':
            self.weekday_heatmap(len)

        else:
            if ptype == 'unique':
                self.weekday_heatmap(self.count_unique)
            else:
                print('{} is not a valid plot type'.format(ptype))


    def read_colormap(self, path='data/rgb.txt'):

        self.color_map = pd.read_csv(path
                                     ,sep='\t'
                                     ,skiprows=[0]
                                     ,names = ['color', 'hex', 'unk'])[['color', 'hex']]




    @check_hash
    def save_data(self, save_path=None):
        if save_path is None:
            min_date = format(self.data.index.min(), '%Y%m%d')
            max_date = format(self.data.index.max(), '%Y%m%d')
            save_path = 'data/from_{}_to_{}.csv'.format(min_date, max_date)
        self.data.to_csv(save_path)


    def summary(self):
        summary_dict = {}

        # Total messages
        summary_dict['total_msg'] = len(self.data)

        # unique user count
        summary_dict['unique_users'] = len(set(self.data.From))

        summary_dict['repeat_users'] = sum(self.data.From.value_counts() > 1)

        summary_dict['dedicated_users'] = sum(self.data.From.value_counts() > 10)

        summary_dict['top_colors'] = self.data.Body.value_counts().head(5).to_json()

        summary_dict['secret_texts'] = sum(self.data.Body == 'secret')
        return summary_dict


    def translate_color(self, color_name):

        try:
            rgb_color = self.color_map[self.color_map.color == difflib.get_close_matches(color_name, self.color_map.color)[0]].hex.to_string(index=False)
        except IndexError:
            rgb_color = '#ffffff'

        except AttributeError:
            self.read_colormap()
            rgb_color = self.translate_color(color_name)

        return rgb_color


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
