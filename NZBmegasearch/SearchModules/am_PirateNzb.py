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
import time
import logging
from collections import OrderedDict

log = logging.getLogger(__name__)



class am_PirateNzb(SearchModule):
    # Set up class variables
    def __init__(self):
        super(am_PirateNzb, self).__init__()
        self.name = 'PirateNZB'
        self.typesrch = 'PIR'
        self.queryURL = 'https://piratenzb.com/api'
        self.baseURL = 'https://piratenzb.com'
        self.active = 0
        self.builtin = 1
        self.login = 1
        self.inapi = 1
        self.api_catsearch = 1
        self.caption_login_user = 'user'
        self.caption_login_pwd = 'api'
        self.agent_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

        self.categories = { #https://piratenzb.com/api?t=caps needs updating
        'Console': {'code': [1000, 1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080], 'pretty': 'Console'},
        'Movie': {'code': [2000, 2010, 2020, 2030, 2040, 250, 2060], 'pretty': 'Movie (ALL)'},
        'Movie_HD': {'code': [2040, 2050, 2060, 2080], 'pretty': 'Movie (HD)'},
        'Movie_SD': {'code': [2030, 2070], 'pretty': 'Movie (SD)'},
        'Audio': {'code': [3000, 3010, 3020, 3030, 3040], 'pretty': 'Audio'},
        'Games': {'code': [4050, ], 'pretty': 'Games'},
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
    def search(self, queryString, cfg): #OMG
        urlParams = OrderedDict(
            apikey=cfg['pwd'],
            t='search',
            #q=queryString,
            o='json',
            extended=1
        )
        try:
            http_result = requests.get(url=self.queryURL, params=urlParams, verify=False)
        except Exception as e:
                print e
                return []
        data = http_result.json()
        parsed_data = []
        for i in xrange(len(data)):
            d1 = {
				'title': data[i]['searchname'],
				'poster': data[i]['fromname'],
				'size': data[i]['size'],
				'url': 'https://piratenzb.com/api?apikey='+cfg['pwd']+'&t=get&id='+ str(data[i]['nzbguid']),
				'filelist_preview': '',
                'group':  data[i]['group_name'],
                'posting_date_timestamp': int(data[i]['postdate']),
				'release_description': 'description',
				'release_comments': 'comments',
                'categ': data[i]['categoryid'],
				'ignore':0,
				'provider':self.baseURL
			}
            parsed_data.append(d1)
        return parsed_data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~



