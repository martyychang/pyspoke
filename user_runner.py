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
    
    def list_requests(self, start=0, limit=25):
        req = urllib.request.Request(
            url= '%s/requests?start=%s&limit=%s' % (_SPOKE_API_BASE_URL,
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

# Grab all requests in Spoke
_spokes = SpokeService(os.environ[_SPOKE_API_KEY_VAR])
_users = []

_list_users_start = 0
_list_users_limit = 10
_has_more_users = True

while _has_more_users:
    _list_users = _spokes.list_users(start=_list_users_start)
    if 'results' in _list_users:
        _users += _list_users['results']
        _list_users_start += _list_users_limit
        _has_more_users = _list_users['total'] > _list_users_start
    else:
        _has_more_users = False

# Write the output to a file
_output_dir = 'tmp'
Path(_output_dir).mkdir(parents=True, exist_ok=True)
with open('tmp/%s.json' % _run_datetime.timestamp(), 'w') as f:
    f.write(json.dumps(_users, indent=4))