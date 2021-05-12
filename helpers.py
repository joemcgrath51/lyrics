from datetime import date, timedelta, datetime

import string


from sklearn.feature_extraction.text import CountVectorizer

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords

import billboard

#nltk.download('wordnet')

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


def get_dates_by_month(year):
    ret = []
    d = date(year=year, month=1, day=1)
    ret.append(d)
    while d.month < 12:
        d = d.replace(month=d.month + 1)
        ret.append(d)
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
