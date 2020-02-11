from datetime import datetime
import json
import os
from pathlib import Path
import urllib.request

_SPOKE_API_BASE_URL = 'https://api.askspoke.com/api/v1'

_SPOKE_API_KEY_VAR = 'SPOKE_API_KEY'
'''The API key used to authenticate with the Spoke API.'''

class SpokeService:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def list_request_types(self, start=0, limit=25):
        req = urllib.request.Request(
            url= '%s/request_types?start=%s&limit=%s' % (_SPOKE_API_BASE_URL,
                                                    start, limit,),
            headers={ 'Api-Key': self.api_key }
        )

        res = urllib.request.urlopen(req)

        return json.loads(res.read())
    
    def list_requests(self, start=0, limit=25):
        req = urllib.request.Request(
            url= '%s/requests?start=%s&limit=%s' % (_SPOKE_API_BASE_URL,
                                                    start, limit,),
            headers={ 'Api-Key': self.api_key }
        )

        res = urllib.request.urlopen(req)

        return json.loads(res.read())
    
    def list_tags(self, start=0, limit=25):
        req = urllib.request.Request(
            url= '%s/tags?start=%s&limit=%s' % (_SPOKE_API_BASE_URL,
                                                    start, limit,),
            headers={ 'Api-Key': self.api_key }
        )

        res = urllib.request.urlopen(req)

        return json.loads(res.read())
    
    def list_teams(self, start=0, limit=25):
        req = urllib.request.Request(
            url= '%s/teams?start=%s&limit=%s' % (_SPOKE_API_BASE_URL,
                                                    start, limit,),
            headers={ 'Api-Key': self.api_key }
        )

        res = urllib.request.urlopen(req)

        return json.loads(res.read())
    
    def list_users(self, start=0, limit=10):
        req = urllib.request.Request(
            url= '%s/users?start=%s&limit=%s' % (_SPOKE_API_BASE_URL,
                                                    start, limit,),
            headers={ 'Api-Key': self.api_key }
        )

        res = urllib.request.urlopen(req)

        return json.loads(res.read())

# Define run-specific variables
_run_datetime = datetime.utcnow()

# Grab all teams in Spoke
_spokes = SpokeService(os.environ[_SPOKE_API_KEY_VAR])
_items = []

_list_items_start = 0
_list_items_limit = 25
_has_more_items = True

while _has_more_items:
    _list_items = _spokes.list_tags(start=_list_items_start, limit=_list_items_limit)
    if 'results' in _list_items:
        _items += _list_items['results']
        _list_items_start += _list_items_limit
        _has_more_items = _list_items['total'] > _list_items_start
    else:
        _has_more_items = False

# Write the output to a file
_output_dir = 'tmp'
Path(_output_dir).mkdir(parents=True, exist_ok=True)
with open('tmp/%s.json' % _run_datetime.timestamp(), 'w') as f:
    f.write(json.dumps(_items, indent=4))