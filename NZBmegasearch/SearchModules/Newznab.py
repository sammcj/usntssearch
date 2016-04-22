# # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## #    
# ~ This file is part of NZBmegasearch by 0byte.
# ~
# ~ NZBmegasearch is free software: you can redistribute it and/or modify
# ~ it under the terms of the GNU General Public License as published by
# ~ the Free Software Foundation, either version 3 of the License, or
# ~ (at your option) any later version.
# ~
# ~ NZBmegasearch is distributed in the hope that it will be useful,
# ~ but WITHOUT ANY WARRANTY; without even the implied warranty of
# ~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# ~ GNU General Public License for more details.
# ~
# ~ You should have received a copy of the GNU General Public License
# ~ along with NZBmegasearch.  If not, see <http://www.gnu.org/licenses/>.
# # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## #
import ConfigParser
from SearchModule import *
from urllib2 import urlparse


# Search on Newznab
class Newznab(SearchModule):
    # Set up class variables
    def __init__(self, configFile=None):
        super(Newznab, self).__init__()
        self.name = 'Newznab'
        self.typesrch = 'NAB'
        self.queryURL = 'xxxx'
        self.baseURL = 'xxxx'
        self.nzbDownloadBaseURL = 'NA'
        self.builtin = 0
        self.inapi = 1
        self.api_catsearch = 1
        self.agent_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

        self.categories = {
        'Console': {'code': [1000, 1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080], 'pretty': 'Console'},
        'Movie': {'code': [2000, 2010, 2020, 2030, 2040, 250, 2060], 'pretty': 'Movie (ALL)'},
        'Movie_HD': {'code': [2040, 2050, 2060], 'pretty': 'Movie (HD)'},
        'Movie_SD': {'code': [2030], 'pretty': 'Movie (SD)'},
        'Audio': {'code': [3000, 3010, 3020, 3030, 3040], 'pretty': 'Audio'},
        'Games': {'code': [100, ], 'pretty': 'Games'},
        'PC': {'code': [4000, 4010, 4020, 4030, 4040, 4050, 4060, 4070], 'pretty': 'PC'},
        'TV': {'code': [5000, 5020], 'pretty': 'TV'},
        'TV_SD': {'code': [5030], 'pretty': 'SD'},
        'TV_HD': {'code': [5040], 'pretty': 'HD'},
        'XXX': {'code': [6000, 6010, 6020, 6030, 6040, 6060, 6070], 'pretty': 'XXX'},
        'Anime': {'code': [5070], 'pretty': 'Anime'},
        'Books': {'code': [7000, 7020], 'pretty': 'Books'},
        'Mags': {'code': [7010], 'pretty': 'Magazines'},
        'Ebook': {'code': [7020], 'pretty': 'Ebook'},
        'Comics': {'code': [7030], 'pretty': 'Comics'},
        }
        self.category_inv = {}
        for key in self.categories.keys():
            prettyval = self.categories[key]['pretty']
            for i in xrange(len(self.categories[key]['code'])):
                val = self.categories[key]['code'][i]
                self.category_inv[str(val)] = prettyval

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    def search_raw(self, queryopt, cfg):
        urlParams = dict(
            queryopt,
            o='xml',
            apikey=cfg['api']
        )
        self.queryURL = cfg['url'] + '/api'
        self.baseURL = cfg['url']

        parsed_data = self.parse_xmlsearch(urlParams, cfg['timeout'])
        return parsed_data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def search(self, queryString, cfg):
        # Get text
        urlParams = dict(
            t='search',
            q=queryString,
            o='xml',
            apikey=cfg['api']
        )
        self.queryURL = cfg['url'] + '/api'
        self.baseURL = cfg['url']

        humanprovider = urlparse.urlparse(cfg['url']).hostname
        self.name = humanprovider.replace("www.", "")
        parsed_data = self.parse_xmlsearch(urlParams, cfg['timeout'], cfg)
        return parsed_data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def checkreturn(self, data):

        retcode = self.default_retcode
        limitpos = data.encode('utf-8').lower().find('<error code="500"')
        if (limitpos != -1):
            mssg = 'Download/Search limit reached ' + self.queryURL
            limitpos_comment = data.encode('utf-8').find('description="')
            if (limitpos_comment != -1):
                mssg = data.encode('utf-8')[limitpos_comment + 13:]
            log.error(mssg)
            retcode = [500, sanitize_strings(mssg).replace(".", " ").capitalize(), 0, '']

        limitpos = data.encode('utf-8').lower().find('<error code="100"')
        if (limitpos != -1):
            mssg = 'Incorrect user credentials ' + self.queryURL
            limitpos_comment = data.encode('utf-8').find('description="')
            if (limitpos_comment != -1):
                mssg = data.encode('utf-8')[limitpos_comment + 13:]
            log.error(mssg)
            retcode = [100, sanitize_strings(mssg).replace(".", " ").capitalize(), 0, '']
        return retcode
