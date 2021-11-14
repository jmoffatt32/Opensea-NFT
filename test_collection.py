from collection import Collection
from pprint import pprint
import requests

owner = '0xca8b73101e12c03e4e9eacf0e180fc10edf859e2'
slug = 'mekaverse'

#mekaverse = Collection(owner = owner, slug = slug)
#pprint(mekaverse.response)

#r = requests.get("https://opensea.io/collection/mekaverse?search[sortAscending]=true&search[sortBy]=PRICE&search[stringTraits][0][name]=Jaws&search[stringTraits][0][values][0]=MI%20WS-1")
r = requests.get("https://api.opensea.io/api/v1/asset/0x9a534628b4062e123ce7ee2222ec20b86e16ca8f/1")
response_json = r.json()
print(r)