import bs4

from CaseBonita.Services.PlaylistDownloader.Handlers.Base import ScraperBaseDownloaderHandler


class AppleMusicDownloaderHandler(ScraperBaseDownloaderHandler):
    @classmethod
    def _read_songs_and_artists(cls, web_page):
        html_soup = bs4.BeautifulSoup(web_page.content, 'html.parser')
        titles_artists = cls._fetch_titles_artists(html_soup)
        artists_songs_json = [cls._parse_title_aritst(title_aritst) for title_aritst in titles_artists]
        return artists_songs_json

    @classmethod
    def _parse_title_aritst(cls, title_artist):
        title = title_artist.find('span',
                                  class_="we-truncate we-truncate--single-line ember-view tracklist-item__text__headline targeted-link__target")
        artist = title_artist.find('a',
                                   class_="table__row__link table__row__link--secondary")
        result = {
            'title': title.text.strip(),
            'artist': artist.text.strip(),
        }
        return result

    @classmethod
    def _fetch_titles_artists(cls, soup):
        """
        :param: bs4.BeautifulSoup soup:
        :rtype: list: List containing title artist object
        """
        title_artist = soup.find_all('div', class_="tracklist-item__text we-selectable-item__link-text")
        return title_artist

