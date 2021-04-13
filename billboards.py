#!/usr/bin/python3
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import helpers

def main():

    years = ['2016', '2017', '2018', '2019' , '2020']
    #years = ['2017', '2018', '2019', '2020']
    years = ['2019' , '2020']
    genre = 'r-b-hip-hop-songs'
    genius = 'QfcNFORWYYHMb2l48a95UsfzXqNTjnbJZkn3TZZ6HTquOw58d7JQdERD8VnOa71y'
    h = helpers.search_data(genius, genre, years)

    words = helpers.count(h)
    helpers.plot_wordcloud(words,2,3)


if __name__ == "__main__":
    main()


