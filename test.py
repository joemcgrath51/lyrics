#!/usr/bin/python3
import warnings
import os
from wordcloud import WordCloud, STOPWORDS

import matplotlib.pyplot as plt

import pandas as pd
import json

import billboard

from lyricsgenius import Genius, song

warnings.simplefilter(action='ignore', category=FutureWarning)
import helpers


def main():

    y = ['1991', '1992', '1993', '1994', '1995',
         '1996', '1997', '1998', '1999', '2000', '2001',
         '2002', '2003', '2004', '2005', '2006', '2007',
         '2008', '2009', '2010', '2011', '2012', '2013',
         '2014', '2015', '2016', '2017', '2018', '2019',
         '2020']
    """y = ['2001',
         '2002', '2003', '2004', '2005', '2006', '2007',
         '2008', '2009', '2010', '2011', '2012', '2013',
         '2014', '2015', '2016', '2017', '2018', '2019',
         '2020']"""

    g = 'QfcNFORWYYHMb2l48a95UsfzXqNTjnbJZkn3TZZ6HTquOw58d7JQdERD8VnOa71y'
    #directory = '/home/joe/Desktop/lyrics/'
    directory = 'D:\Downloads\\lyrics-main\\lyrics-main\\'
    h = Genius(g)

    createFolders(y)
    genre = 'r-b-hip-hop-songs'
    #"""
    for i in range(len(y)):

        dir = directory + y[i]

        charts = helpers.get_charts(genre, dates=helpers.get_dates_by_month(int(y[i])))
        n = helpers.get_n_most_frequent_entries(charts, 100)

        for x in range(len(n)):

            name = n[x].split(",")[0]

            if "'" in name:
                name = name.replace("'", "’")

            if not os.path.exists(dir + '/' + name + '.json'):
                r = h.search_song(n[x])

                if r is None:
                    continue

                print(r.title)
                print(name)
                print(r.title.lower() not in name.lower())

                print(type(r))
                if r.title.lower() not in name.lower():
                    continue

                if "/" in name:
                    name = name.replace("/", " ")

                #r.save_lyrics(filename=name, full_data=False, dic=dir,
                              #overwrite=True)
                r.save_lyrics(filename=name, dic=dir,
                              overwrite=True)
    #"""
    df = readFiles(directory, y)

    years = []
    for i in range(len(df)):
        temp = []
        for x in range(len(df[i]['words'])):
            temp.append(','.join(df[i]['words'][x]).lower())
        years.append(temp)

    plt.figure()
    wc = []
    stop_words = ['im', 'got', 'yeah', 'na', 'oh', 'know', 'see']

    STOPWORDS.update(stop_words)

    for x in range(len(y)):
        j = x + 1
        print(len(years[x]))

        wc.append(WordCloud(background_color="white", max_font_size=300, collocations=True, stopwords=STOPWORDS))
        wc[x].generate(str(years[x]))
        plt.subplot(int(str(len(y))[:1]) * 2, 5, j).set_title(y[x])

        plt.plot()
        plt.imshow(wc[x], interpolation='bilinear')
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
