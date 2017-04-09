import pandas as pd


def read_data():
    df = pd.read_csv('data/NAPA_Color-Commons-Data-Anon_2_14_2017_to_3_31_2017.csv')

    df['datetime'] = pd.to_datetime(df.SentDate)
    df['date'] = [x.date() for x in df.datetime]
    df['weekday'] = [x.weekday() for x in df.datetime]
