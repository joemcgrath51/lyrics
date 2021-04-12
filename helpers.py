from datetime import date, timedelta, datetime
import os

import lyricsgenius as genius
import pandas as pd
import string 

from sklearn.feature_extraction.text import CountVectorizer

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
from pandas import unique

import billboard

#nltk.download('wordnet')

def search_data(access_token,genre,year):
    """
    This function uses the library lyricsgenius to extract the fields
    title, artist, album, date and lyrics and stores them into a pandas dataframe

    parameters:
    query = artist or band to search
    n = max numbers of songs
    access_token = your access token of the genius api
    """
    list_lyrics = []
    list_title = []
    list_artist = []
    list_album = []
    list_year = []
    words =[]

    api = genius.Genius(access_token)
    for x in range(len(year)):
        charts = get_charts(genre, dates=get_dates_by_month(int(year[x])))
        top_songs = get_n_most_frequent_entries(charts, 5)

        for song in top_songs:
            s = song.split(',')
            if "Featuring" in s[1]:
                s[1] = s[1].split("Featuring")

            track = api.search_song(s[0], s[1][0])
            if track is not None:
                list_lyrics.append(track.lyrics)
                list_title.append(track.title)
                list_artist.append(track.artist)
                list_album.append(track.album)
                list_year.append(year[x])

    df = pd.DataFrame({'artist':list_artist,'title':list_title,'album':list_album,
                        'year':list_year,'lyric':list_lyrics})
    df = clean_lyrics(df, 'lyric')
    df = df.reset_index(drop=True)

    for word in df['lyric'].tolist():
        if not str(word).isdigit():
            words.append(unique(lyrics_to_words(word).split()))

    df['words'] = words
    return df


def clean_lyrics(df,column):
    """
    This function cleans the words without importance and fix the format of the  dataframe's column lyrics 

    parameters:
    df = dataframe
    column = name of the column to clean
    """
    df = df
    df[column] = df[column].str.lower()
    df[column] = df[column].str.replace(r"verse |[1|2|3]|chorus|bridge|outro|verse","").str.replace("[","").str.replace("]","")
    df[column] = df[column].str.lower().str.replace(r"instrumental|intro|guitar|solo","")
    df[column] = df[column].str.replace("\n"," ").str.replace(r"[^\w\d'\s]+","").str.replace("efil ym fo flah","")
    df[column] = df[column].str.strip()

    return df


def lyrics_to_words(document):
    """
    This function splits the text of lyrics to  single words, removing stopwords and doing the lemmatization to each word

    parameters:
    document: text to split to single words
    """
    stop_words = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    stopwordremoval = " ".join([i for i in document.lower().split() if i not in stop_words])
    punctuationremoval = ''.join(ch for ch in stopwordremoval if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punctuationremoval.split())
    return normalized


def create_decades(df):
    """
    This function creates a new column called decades used to group the songs and lyrics by decade based on the date released 
    for each song

    parameters:
    df = dataframe
    """
    years = []
    decades = []
    df['date'].fillna(0)
    df['date'] = df['date'].astype("str")
    for i in df.index:
        years.append(df['date'].str.split("-")[i][0])
    df['year'] = years
    df['year'] = df['year'].astype("int")

    for year in df['year']:
        if 1970 <= year < 1980:
            decades.append("70s")
        if 1980 <= year < 1990:
            decades.append("80s")
        if 1990 <= year < 2000:
            decades.append("90s")
        if 2000 <= year < 2010:
            decades.append("00s")
        if 2010 <= year :
            decades.append("10s")
    df['decade'] = decades
    df = df[['artist','title','album','decade','year','date','lyric']]
    return df


def get_dates_by_month(year):
    ret = []
    d = date(year=year, month=1, day=1)
    ret.append(d)
    while d.month < 12:
        d = d.replace(month=d.month + 1)
        ret.append(d)
    return ret


def get_dates_by_week(year):
    ret = []
    d = date(year=year, month=1, day=1)
    delta = timedelta(days=7)
    while d.year == year:
        ret.append(d)
        d = d + delta
    return ret


def get_chart_entries(playlist, date):
    chart = billboard.ChartData(playlist, str(date))
    delta = timedelta(days=1)
    total_delta = timedelta(days=0)
    while len(chart.entries) == 0:
        total_delta += delta
        chart = billboard.ChartData(playlist, str(date + total_delta))
    return (chart, total_delta)


def get_charts(playlist, dates):
    ret = []
    delta = timedelta(days=0)
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

    l = [(k, v) for k, v in d.items()]
    l.sort(key=lambda x: x[1])
    l.reverse()

    return [title for title, freq in l[:n]]


def count(df):
    set_words = []
    set_years = []
    for i in df.index:
        for word in df['words'].iloc[i]:
            set_words.append(word)
            set_years.append(df['year'].iloc[i])

    print(set_years)
    words_df = pd.DataFrame({'words': set_words,'year':set_years})
    # count the frequency of each word that aren't on the stop_words
    cv = CountVectorizer() # Create a dataframe called data_cv to store the the number of times the word was used in  a lyric based their decade
    text_cv = cv.fit_transform(words_df['words'].iloc[:])


    data_cv = pd.DataFrame(text_cv.toarray(), columns=cv.get_feature_names())
    data_cv['year'] = words_df['year']

    vect_words = data_cv.groupby('year').sum().T
    vect_words = vect_words.reset_index(level=0).rename(columns={'index': 'words'})
    vect_words = vect_words.rename_axis(columns='')

    vect_words.to_csv('words.csv', index=False)
    vect_words = vect_words[['words', '2018', '2019']]
    return vect_words