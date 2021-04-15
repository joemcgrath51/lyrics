#!/usr/bin/python3
import warnings
import os
import matplotlib.pyplot as plt


import lyricsgenius.song
import pandas as pd
import json

import billboard

from lyricsgenius import Genius
from lyricsgenius import song

warnings.simplefilter(action='ignore', category=FutureWarning)
import helpers

def main():

    years = ['2016', '2017', '2018', '2019', '2020']
    #years = ['2019', '2020']
    years = ['2020']
    genre = 'r-b-hip-hop-songs'
    g = 'QfcNFORWYYHMb2l48a95UsfzXqNTjnbJZkn3TZZ6HTquOw58d7JQdERD8VnOa71y'
    directory = '/home/joe/Desktop/lyrics/'
    h = Genius(g)

    createFolders(years)

    for i in range(len(years)):

        dir = directory + years[i]
        r = billboard.ChartData('hot-r-and-and-b-hip-hop-songs', date=None, year=years[i], fetch=False)

        r.fetchEntries()
        try:
            for x in range(len(r)):
                if 'Featuring' in r[x].artist:
                    r[x].artist = r[x].artist.split('Featuring')[0]
                if os.path.exists(dir + '/' + r[x].title + '.json'):
                    continue
                else:
                    s = h.search_song(r[x].title, artist=r[x].artist)
                    s.save_lyrics(filename=r[x].title, full_data=False, dic=dir, overwrite=True)

        except Exception as e:
            print(e)
    df = readFiles(directory, years)

    temp = helpers.count(df)

    helpers.plot_wordcloud(temp, 3, 3)

def createFolders(years):
    for x in range(len(years)):
        if not os.path.exists(years[x]):
            os.makedirs(years[x])


def readFiles(dir, year):

    frames = []

    for i in range(len(year)):
        list_lyrics = []
        list_title = []
        list_year = []
        words = []
        files = os.listdir(dir + year[i])
        for x in range(len(files)):
            with open(dir + year[i] + '/' + files[x]) as train_file:
                dict_train = json.load(train_file)
                list_title.append(dict_train['title'])
                list_lyrics.append(dict_train['lyrics'])
                list_year.append(year[i])

        df = pd.DataFrame({'year': list_year, 'title': list_title, 'lyrics': list_lyrics})

        df = helpers.clean_lyrics(df, 'lyrics')
        df = df.reset_index(drop=True)

        for word in df['lyrics'].tolist():
            if not str(word).isdigit():
                words.append(helpers.lyrics_to_words(word).split())
        df['words'] = words
        frames.append(df)
        del df

    return frames


if __name__ == "__main__":
    main()


