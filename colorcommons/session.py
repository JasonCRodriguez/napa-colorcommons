# coding: utf-8
df["date"].groupby(df["date"]).count().plot(kind="bar")
df = pd.read_csv('data/NAPA_Color-Commons-Data-Anon_2_14_2017_to_3_31_2017.csv')
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv('data/NAPA_Color-Commons-Data-Anon_2_14_2017_to_3_31_2017.csv')
df.datetime
df['datetime'] = pd.to_datetime(df.SentDate)
df['date'] = [x.date() for x in df.datetime]
df['weekday'] = [x.weekday() for x in df.datetime]
df.to_csv('data/napa_with_datetime.csv')
df
df["date"].groupby(df["date"]).count().plot(kind="bar", fill=df.weekday)
df["date"].groupby(df["date", 'weekday']).count().plot(kind="bar", fill=df.weekday)
df["date"].groupby(df["date", 'weekday']).count().plot(kind="bar")
df["date", "weekday"].groupby(df["date", "weekday"]).count().plot(kind="bar")
df[["date", "weekday"]].groupby(df["date", "weekday"]).count().plot(kind="bar")
df[["date", "weekday"]].groupby(["date", "weekday"]).count().plot(kind="bar")
df[["date", "weekday"]].groupby("date").count().plot(kind="bar")
plt.show()
df[["date", "weekday"]].groupby("date").count().plot(kind="bar", color='weekday')
colors = {1:'red', 2:'blue', 0:'green', 4:'black'}
df[["date", "weekday"]].groupby("date").count().plot(kind="bar", color=colors)
df[["date", "weekday"]].groupby("date").count().plot(kind="bar", stacked=True)
plt.show()
df[["date", "weekday"]].groupby(["date", "weekday"]).count().plot(kind="bar", stacked=True)
df[["date", "weekday"]].groupby("date").count()
grp = df[["date", "weekday"]].groupby("date").count()
grp
grp.head()
grp = df[["date", "weekday"]].groupby("date")
grp
grp.head()
grp.head(5)
grp = df[["date", "weekday", "id"]].groupby("date")
grp.count()
grp.count().head()
grp.aggregate({'weekday':mode, 'id':len})
grp.aggregate({'weekday':max, 'id':len})
grp.aggregate({'weekday':max, 'id':len}).plot(type='bar', stacked=True)
grp.aggregate({'weekday':max, 'id':len}).plot(type='bar', y='id', stacked=True)
grp.aggregate({'weekday':max, 'id':len}).plot(type='bar')
grp.aggregate({'weekday':max, 'id':len}).plot(x = 'date', type='bar')
grp.aggregate({'weekday':max, 'id':len}).plot(type='bar')
get_ipython().magic('save napa/prep.py 1-45')
