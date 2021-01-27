#!/usr/bin/python2.7
import os

import billboard

from lyricsgenius import Genius
from datetime import date
from datetime import timedelta
from datetime import datetime
import argparse

def get_dates_by_month(year):
    ret = []
    d = date(year = year, month = 1, day = 1)
    ret.append(d)
    while d.month < 12:
        d = d.replace(month = d.month + 1)
        ret.append(d)
    return ret


def get_dates_by_week(year):
    ret = []
    d = date(year = year, month = 1, day = 1)
    delta = timedelta(days = 7)
    while d.year == year:
        ret.append(d)
        d = d + delta
    return ret

def get_chart_entries(playlist, date):
    chart = billboard.ChartData(playlist, str(date))
    delta = timedelta(days = 1)
    total_delta = timedelta(days = 0)
    while len(chart.entries) == 0:
        total_delta += delta
        chart = billboard.ChartData(playlist, str(date + total_delta))
    return (chart, total_delta)


def get_charts(playlist, dates):
    ret = []
    delta = timedelta(days = 0)
    for d in dates:
        if d > datetime.today().date():
            continue
        chart, delta = get_chart_entries(playlist, d + delta)
        ret.append(chart)
    return ret

def get_n_most_frequent_entries(charts, n):
    d = {}
    for chart in charts:
        for song in chart.entries:
            key = song.title + "," + song.artist
            if key not in d:
                d[key] = 1
            else:
                d[key] += 1

    l = [(k,v) for k,v in d.items()]
    l.sort(key=lambda x: x[1])
    l.reverse()
    
    return [title for title,freq in l[:n]]

def main():
    genius = Genius('QfcNFORWYYHMb2l48a95UsfzXqNTjnbJZkn3TZZ6HTquOw58d7JQdERD8VnOa71y')

    years = ['2000', '2001', '2002', '2003', '2004']
    for x in range(len(years)):
        charts = get_charts('r-b-hip-hop-songs',dates = get_dates_by_month(int(years[x])))
        top_songs = get_n_most_frequent_entries(charts, 10)

        for song in top_songs:
            s = song.split(',')
            track = genius.search_song(s[0],s[1])
            filename = 'songs/' + years[x] + '/' + track.title + '.txt'
            os.makedirs(os.path.dirname(filename), exist_ok = True)
            with open(filename, "w") as text_file:
                print(track.lyrics, file=text_file)


if __name__ == "__main__":
    main()


