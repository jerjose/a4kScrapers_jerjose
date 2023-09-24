# -*- coding: utf-8 -*-
import time

from providerModules.a4kScrapers import core
from bs4 import BeautifulSoup
import re

class sources(core.DefaultSources):
    def __init__(self, *args, **kwargs):
        super(sources, self).__init__(__name__, *args, single_query=True, **kwargs)
        self._filter = core.Filter(fn=self._filter_fn, type='single')

    def _get_scraper(self, title):
        return super(sources, self)._get_scraper(title, custom_filter=self._filter)

    def _info(self, el, url, torrent):
        torrent['size'] = core.source_utils.de_string_size(el.size)
        torrent['seeds'] = el.seeds
        torrent['magnet'] = el.magnet
        torrent['hash'] = el.hash

        return torrent

    def _filter_fn(self, title, clean_title):
        if self.is_movie_query():
            return True

    def _title_filter(self, el):
        return el.title

    def _soup_filter(self, response):
        rsp_data = str(self._extract_movielinks(response))
        rsp_data = core.normalize(rsp_data)
        results = self.genericScraper._parse_rows(rsp_data,row_tag=',')
        return results

    def _search_request(self, url, query):
        query = core.quote(" ".join(self._title_arr)+" "+self._year)
        response = self._request.get(url.base + url.search + query)

        if response.status_code != 200:
            return []

        rsp_data = self._extract_movielinks(response)

        if not rsp_data:
            self._alternate_search = True
            search = "/index.php?/search/&search_and_or=or&search_in=titles&sortby=relevancy&q="
            time.sleep(5)
            response = self._request.get(url.base + search + query)
            rsp_data = self._extract_movielinks(response)

        if not rsp_data:
            return []

        return response

    def movie(self, title, year, imdb=None, **kwargs):
        self._title = str(title).strip()
        self._title_arr = self._searchable_title(self._title)
        self._title_first_word = self._title_arr[0]
        self._year = str(year).strip()
        self._imdb = imdb
        self._alternate_search = False
        return super(sources, self).movie(self._title, self._year, self._imdb)

    def _searchable_title(self, title):
        title_str = title.strip()
        title_str = re.sub(r'[^0-9a-zA-Z]+', ' ', title_str)
        return title_str.split()


    def _extract_movielinks(self,response):
        magnetic_links = []

        # Parse the response content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all the elements that contain the data you want
        # movie links belong to topic
        if not self._alternate_search:
            links = soup.find_all('a', href=re.compile('topic.*' + '.*'.join(self._title_arr) + '.*' + self._year, re.IGNORECASE))
        else:
            links = soup.find_all('a', href=re.compile('topic.*' + '(' + '|'.join(self._title_arr) + ')' + '.*' + self._year, re.IGNORECASE))

        # Loop through the links elements and print their href attribute
        for link in links:
            if link.has_attr('href'):
                # print(link.get('href'))
                rsp = self._request.get(link.get('href'))
                bs = BeautifulSoup(rsp.content, "html.parser")
                # Find all the elements that contain the magnetic links
                mg_lns = bs.find_all("a", href=re.compile('^magnet', re.IGNORECASE))
                for ln in mg_lns:
                    if (ln.has_attr('href')):
                        magnetic_links.append(ln)

        return magnetic_links
