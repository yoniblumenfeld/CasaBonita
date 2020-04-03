# import bs4
#
# from CaseBonita.Services.PlaylistDownloader.Handlers.Base import ScraperBaseDownloaderHandler
#
#
# class AppleMusicDownloaderHandler(ScraperBaseDownloaderHandler):
#     @classmethod
#     def _read_songs_and_artists(cls, web_page):
#         html_soup = bs4.BeautifulSoup(web_page.content, 'html.parser')
#         titles_artists = cls._fetch_titles_artists(html_soup)
#
#         titles = parse_title(titles_artists.find('span', class_="we-truncate we-truncate--single-line ember-view tracklist-item__text__headline targeted-link__target").text
#         artist = titles_artists.find('a', class_="table__row__link table__row__link--secondary").text
#         print(title)
#         print(artist)
#         titles = html_soup.find_all('div', class_="tracklist-item_artwork")
#
#     @classmethod
#     def _fetch_titles_artists(cls, soup):
#         """
#         :param: bs4.BeautifulSoup soup:
#         :rtype: list: List containing title artist object
#         """
#         title_artist = soup.find_all('div', class_="tracklist-item__text we-selectable-item__link-text")
#         return title_artist
#
#     def parse_title(self, title):
#         for t in titles:
#             t.strip()
#