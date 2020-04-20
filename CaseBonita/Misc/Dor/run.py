from CaseBonita.Utils.Platforms.Spotify.DataUtils import ExtraDataFetcher

if __name__ == '__main__':
    f = ExtraDataFetcher()
    di = f.add_tracks_ids(playlist=[
        {"Redbone": "Childish Gambino"},
        {"Flipside": "Ripe"}])
    print(di)