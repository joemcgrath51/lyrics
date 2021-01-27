from lyricsgenius import Genius


def main():
    genius = Genius('QfcNFORWYYHMb2l48a95UsfzXqNTjnbJZkn3TZZ6HTquOw58d7JQdERD8VnOa71y')

    artist = genius.search_artist('Drake', max_songs=3, sort='popularity', get_full_info=False)

    print(artist.songs)
    with open("Output.txt", "w") as text_file:
        print(artist.songs
, file=text_file)


if __name__ == "__main__":
    main()
