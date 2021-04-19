#!/usr/bin/python3
import warnings
import os
from wordcloud import WordCloud

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

    #years = ['2016', '2017', '2018', '2019', '2020']
    years = ['2019', '2020']
    #years = ['2020']
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
    #year2019 = df[0]['words']
    #year2019 = year2019.tolist()
    print(len(df[0]['words']))
    for i in range(len(df)):
        temp = []
        for x in range(len(df[i]['words'])):
            temp.append(','.join(df[0]['words'][x]).lower())
        years.append(temp)

    print(years[2])
    print("------------------------------------------------------------------------")
    print(years[3])

    plt.figure()
    wc = []
    for x in range(len(years) - 2):
        j = x + 2
        wc.append(WordCloud(background_color="white", max_font_size=100, collocations=True))
        wc[x].generate(str(years[j]))
        plt.subplot(1, 4, j).set_title("Topic #" + str(x))
        plt.plot()
        plt.imshow(wc[x], interpolation='bilInear')
        plt.axis('off')
    plt.suptitle("Year")
    plt.show()
        #temp = helpers.count(df)

    #helpers.plot_wordcloud(temp, 2, 2)

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


