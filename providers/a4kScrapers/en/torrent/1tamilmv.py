# -*- coding: utf-8 -*-

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
        torrent['size'] = el['size']
        torrent['seeds'] = el['seeds']
        torrent['magnet'] = el['magnet']
        torrent['hash'] = el['hash']

        return torrent

    def _filter_fn(self, title, clean_title):
        core.tools.log("jerrin 1tamilmv _filter_fn " + str(self.is_movie_query()), 'notice')
        if self.is_movie_query():
            return True

    def _title_filter(self, el):
        return el['title']

    def _soup_filter(self, response):
        rsp_data = str(self._extract_movielinks(response))
        core.tools.log("jerrin 1tamilmv rsp_data " + rsp_data, 'notice')
        rsp_data = core.normalize(rsp_data)
        core.tools.log("jerrin 1tamilmv normalize rsp_data" + rsp_data, 'notice')
        results = self.genericScraper._parse_rows(rsp_data,row_tag=',')
        return results

    def _search_request(self, url, query):
        query = core.quote(" ".join(self._title_arr)+" "+self._year)
        core.tools.log("jerrin 1tamilmv query " + str(query), 'notice')
        core.tools.log("jerrin 1tamilmv url " + url.base + url.search + query,'notice')
        response = self._request.get(url.base + url.search + query)

        core.tools.log("jerrin 1tamilmv response " + str(response), 'notice')
        core.tools.log("jerrin 1tamilmv response " + str(response.text), 'notice')

        if response.status_code != 200:
            return []

        #type(response).text = str(self._extract_movielinks(response))

        core.tools.log("jerrin 1tamilmv response " + str(response.text), 'notice')

        return response

    def movie(self, title, year, imdb=None, **kwargs):
        self._title = str(title).strip()
        self._title_arr = self._searchable_title(self._title)
        self._title_first_word = self._title_arr[0]
        core.tools.log("jerrin 1tamilmv _title_arr " + str(self._title_arr) + " _title_first_word " + self._title_first_word, 'notice')
        self._year = str(year).strip()
        self._imdb = imdb
        return super(sources, self).movie(self._title, self._year, self._imdb)

    def _searchable_title(self, title):
        title_str = title.strip()
        title_str = re.sub(r'[^0-9a-zA-Z]+', ' ', title_str)
        core.tools.log("jerrin 1tamilmv title_str " + title_str,'notice')
        return title_str.split()


    def _extract_movielinks(self,response):
        magnetic_links = []

        core.tools.log("jerrin 1tamilmv _extract_movielinks", 'notice')
        # Parse the response content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all the elements that contain the data you want
        links = soup.find_all('a', href=re.compile('.*'.join(self._title_arr) + '.*' + self._year,re.IGNORECASE))

        core.tools.log("jerrin 1tamilmv links " + str(links),'notice')

        # Loop through the links elements and print their href attribute
        for link in links:
            if link.has_attr('href'):
                # print(link.get('href'))
                rsp = self._request.get(link.get('href'))
                bs = BeautifulSoup(rsp.content, "html.parser")
                # Find all the elements that contain the magnetic links
                #mg_lns = bs.find_all("a", href=re.compile('^magnet.*' + self._title_first_word, re.IGNORECASE))
                mg_lns = bs.find_all("a", href=re.compile('^magnet', re.IGNORECASE))
                for ln in mg_lns:
                    if (ln.has_attr('href')):
                        magnetic_links.append(ln)

        return magnetic_links
