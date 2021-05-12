#!/usr/bin/python3
import warnings
import os
import matplotlib.pyplot as plt
import pandas as pd
import json
import helpers
from wordcloud import WordCloud, STOPWORDS
from lyricsgenius import Genius

warnings.simplefilter(action='ignore', category=FutureWarning)

# Add/Remove words you care about
stopwords = ['im', 'got', 'yeah', 'na',
             'oh', 'know', 'see', 'ayy',
             'way', 'aint', 'ill', 'cant',
             'want', 'let', 'say', 'back',
             'cause', 'gon', 'go', 'uh',
             'make', 'versace', 'put',
             'thoia', 'ya', 'hol', 'thats',
             'wanna']

# Add/Remove years you want displayed
years = ['1991', '1992', '1993', '1994', '1995',
         '1996', '1997', '1998', '1999', '2000', '2001',
         '2002', '2003', '2004', '2005', '2006', '2007',
         '2008', '2009', '2010', '2011', '2012', '2013',
         '2014', '2015', '2016', '2017', '2018', '2019',
         '2020']


g_token = 'QfcNFORWYYHMb2l48a95UsfzXqNTjnbJZkn3TZZ6HTquOw58d7JQdERD8VnOa71y'
genius_api = Genius(g_token)

# Genre you care about, you'll need to delete all year folders before changing genre
genre = 'r-b-hip-hop-songs'


# Directory that the program is in
# directory = '/home/joe/Desktop/lyrics/'                       # Linux format
directory = "D:\\Users\Joe\Desktop\GitHub\lyrics\\"             # Windows format


def main():
    # Creates folders to holder songs
    create_folders()

    # Fetches the songs and stores them into a json file
    # Only need to run this function if want more years
    #get_songs()

    # Reads the json files and stores them in a panda
    df = read_files()

    # Counts the lyrics
    y = count(df)

    # Displays the lyrics by order of appearance
    display(y)


def get_songs():
    for i in range(len(years)):

        dir = directory + years[i]

        charts = helpers.get_charts(genre, dates=helpers.get_dates_by_month(int(years[i])))
        n = helpers.get_n_most_frequent_entries(charts, 100)

        for x in range(len(n)):

            name = n[x].split(",")[0]
            artist = n[x].split(',')[1]
            temp = name + ',' + artist

            if "'" in name:
                name = name.replace("'", "’")

            if not (os.path.exists(dir + '/' + name + '.json') or os.path.exists(dir + '/' + temp + '.json')):
                r = genius_api.search_song(n[x])

                if r is None:
                    continue

                if r.title.lower() not in name.lower():

                    r = genius_api.search_song(title=temp)
                    if r is None:
                        continue

                    if r.title.lower() not in name.lower():
                        continue

                    if "/" in temp:
                        temp = temp.replace("/", " ")
                    if '?' in temp:
                        temp = temp.replace("?", "")

                    r.save_lyrics(filename=temp, full_data=False, dic=dir,
                                  overwrite=True)
                    continue

                if "/" in name:
                    name = name.replace("/", " ")

                if '?' in name:
                    name = name.replace("?", "")
                print(dir+'\\'+name)

                r.save_lyrics(filename=dir + '\\' + name,
                              overwrite=True)


def count(df):
    y = []
    for i in range(len(df)):
        temp = []
        for x in range(len(df[i]['words'])):
            temp.append(','.join(df[i]['words'][x]).lower())
        y.append(temp)
    return y


def display(n):
    plt.figure()
    wc = []

    STOPWORDS.update(stopwords)

    for x in range(len(years)):
        j = x + 1
        print(str(years[x]) + ": ", len(n[x]))

        wc.append(WordCloud(background_color="white",
                            min_font_size=10,
                            max_font_size=400,
                            collocations=True,
                            max_words=10,
                            stopwords=STOPWORDS,
                            contour_color='#5d0f24',
                            contour_width=3))
        wc[x].generate(str(n[x]))
        plt.subplot(int(str(len(years))[:1]) * 2, 5, j).set_title(years[x])

        plt.plot()
        plt.imshow(wc[x], interpolation='bilinear')
        plt.axis('off')

    plt.suptitle("Lyrics")
    plt.show()


def create_folders():
    for x in range(len(years)):
        if not os.path.exists(years[x]):
            os.makedirs(years[x])


def read_files():
    frames = []

    for i in range(len(years)):
        list_lyrics = []
        list_title = []
        list_year = []
        words = []
        files = os.listdir(directory + years[i])
        for x in range(len(files)):
            with open(directory + years[i] + '/' + files[x]) as train_file:
                dict_train = json.load(train_file)
                list_title.append(dict_train['title'])
                list_lyrics.append(dict_train['lyrics'])
                list_year.append(years[i])

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
