import requests
from requests.models import Response

class Collection:
    def __init__(self, owner, slug):
        params = {
            'asset_owner' : owner, 
        }
        self.response_json = requests.get('https://api.opensea.io/api/v1/collections', params = params).json()
        for r in self.response_json:
            if slug == r['slug']:
                self.collection_json = r

    def get_collection_count(self):
        return self.collection_json['stats']['count']












