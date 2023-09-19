# -*- coding: utf-8 -*-

from providerModules.a4kScrapers import core

class sources(core.DefaultSources):
    def __init__(self, *args, **kwargs):
        super(sources, self).__init__(__name__, *args, single_query=True, **kwargs)

    def _search_request(self, url, query):
        query = core.quote(" ".join([self._title,self._year]))
        core.tools.log("jerrin tamilblasters query " + str(query), 'notice')
        core.tools.log("jerrin tamilblasters url " + url.base + url.search + query,'notice')
        response = self._request.get(url.base + url.search + query)

        core.tools.log("jerrin tamilblasters response " + str(response.text), 'notice')

        if response.status_code != 200:
            return []

        try:
            results = core.json.loads(response.text)
        except Exception as e:
            self._request.exc_msg = 'Failed to parse json: %s' % response.text
            return []

        if len(results) == 0 or results[0]['id'] == '0':
            return []
        else:
            return results

    def movie(self, title, year, imdb=None, **kwargs):
        self._title = title
        self._year = year
        self._imdb = imdb
        return super(sources, self).movie(title, year, imdb, auto_query=False)
