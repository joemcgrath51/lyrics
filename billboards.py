#!/usr/bin/python3
import warnings
import os

import lyricsgenius.song
import pandas as pd
import json

import billboard

from lyricsgenius import Genius
from lyricsgenius import song

warnings.simplefilter(action='ignore', category=FutureWarning)
import helpers

def main():

    #years = ['2016', '2017', '2018', '2019' , '2020']
    years = ['2019', '2020']
    genre = 'r-b-hip-hop-songs'
    g = 'QfcNFORWYYHMb2l48a95UsfzXqNTjnbJZkn3TZZ6HTquOw58d7JQdERD8VnOa71y'

    h = Genius(g)
    #h = helpers.search_data(genius, genre, years)


    #words = helpers.count(h)
    #helpers.plot_wordcloud(words,2,3)
    r = []

    createFolders(years)

    for i in range(len(years)):
        directory = '/home/joe/Desktop/lyrics/'
        directory = directory + years[i]
        r = billboard.ChartData('hot-r-and-and-b-hip-hop-songs', date=None, year=years[i], fetch=False)

        r.fetchEntries()
        try:
            for x in range(len(r)):
                if 'Featuring' in r[x].artist:
                    r[x].artist = r[x].artist.split('Featuring')[0]
               # print(directory + '/' + r[x].title)
                if os.path.exists(directory + '/' + r[x].title + '.json'):
                    continue
                else:
                    s = h.search_song(r[x].title, artist=r[x].artist)
                    s.save_lyrics(filename=r[x].title, full_data=False, dic=directory,overwrite=True)

        except Exception as e:
            print(e)

    df = readFiles(directory)
    #print(df)

def createFolders(years):
    for x in range(len(years)):
        if not os.path.exists(years[x]):
            os.makedirs(years[x])

def readFiles(dir):
    files = os.listdir(dir)
    final = pd.DataFrame()

    for x in range(len(files)):
        with open(dir + '/' + files[x]) as train_file:
            print(train_file.name)
            #dict_train = json.load(train_file)
            df = pd.read_json(train_file)
            print(df)
        #df = pd.read_json(train_file.name, orient='index')
        #df = pd.DataFrame.from_dict(dict_train, orient='index'))
        # converting json dataset from dictionary to dataframe
        #df.reset_index(level=0, inplace=True)
        #print(df.iloc[3].array)
        #df = df.transpose()
        #print(df)

    return final

if __name__ == "__main__":
    main()


