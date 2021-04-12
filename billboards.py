#!/usr/bin/python2.7
import os

from pandas import unique

import helpers


def main():
    h = []
    years = ['2000', '2001', '2002', '2003', '2004']
    genre = 'r-b-hip-hop-songs'
    genius = 'QfcNFORWYYHMb2l48a95UsfzXqNTjnbJZkn3TZZ6HTquOw58d7JQdERD8VnOa71y'
    for x in range(len(years)):
        h.append(helpers.search_data(genius, genre, years[x]))
        print(h[x])


if __name__ == "__main__":
    main()


