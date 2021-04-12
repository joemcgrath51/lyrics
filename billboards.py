#!/usr/bin/python3
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import helpers

def main():

    years = ['2018', '2019' , '2020']
    genre = 'r-b-hip-hop-songs'
    genius = 'QfcNFORWYYHMb2l48a95UsfzXqNTjnbJZkn3TZZ6HTquOw58d7JQdERD8VnOa71y'
    h = helpers.search_data(genius, genre, years)

    print(helpers.count(h))


if __name__ == "__main__":
    main()


