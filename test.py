#!/usr/bin/python3
import warnings
import os
from wordcloud import WordCloud, STOPWORDS

import matplotlib.pyplot as plt

import pandas as pd
import json

import billboard

from lyricsgenius import Genius

warnings.simplefilter(action='ignore', category=FutureWarning)
import helpers


def main():
    y = ['2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
        '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    genre = 'hot-r-and-and-b-hip-hop-songs'
    g = 'QfcNFORWYYHMb2l48a95UsfzXqNTjnbJZkn3TZZ6HTquOw58d7JQdERD8VnOa71y'
    directory = '/home/joe/Desktop/lyrics/'
    h = Genius(g)

    createFolders(y)

    for i in range(len(y)):

        dir = directory + y[i]
        r = billboard.ChartData(genre, date=None, year=y[i], fetch=False)

        r.fetchEntries()
        for x in range(len(r)):
            if ',' in r[x].artist:
                r[x].artist = r[x].artist.split(',')[0]

            if '/' in r[x].title:
                r[x].title = r[x].title.replace('/', '')

            if '*' in r[x].title:   # Couldn't find how to remove profanity filter
                continue

            if '(' in r[x].title:
                r[x].title = r[x].title.split('(')[0].rstrip()

            if 'Featuring' in r[x].artist:
                r[x].artist = r[x].artist.split('Featuring')

            if os.path.exists(dir + '/' + r[x].title + '.json'):
                continue

            s = h.search_song(r[x].title, artist=r[x].artist[0])
            l = 0

            while s is None:
                l =+ 1
                s = h.search_song(r[x].title, artist=r[x].artist[l])
                if l > len(r[x].artist):
                    break

            s.save_lyrics(filename=r[x].title, full_data=False, dic=dir, overwrite=True)

    df = readFiles(directory, y)

    years = []
    for i in range(len(df)):
        temp = []
        for x in range(len(df[i]['words'])):
            temp.append(','.join(df[i]['words'][x]).lower())
        years.append(temp)

    plt.figure()
    wc = []
    stop_words = ['im', 'got', 'yeah']

    STOPWORDS.update(stop_words)

    for x in range(len(y)):
        j = x + 1
        print(len(years[x]))

        wc.append(WordCloud(background_color="white", max_font_size=300, collocations=True, stopwords=STOPWORDS))
        wc[x].generate(str(years[x]))
        plt.subplot(2, 5, j).set_title(y[x])
        plt.plot()
        plt.imshow(wc[x], interpolation='bilInear')
        plt.axis('off')

    plt.suptitle("Lyrics")
    plt.show()

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


