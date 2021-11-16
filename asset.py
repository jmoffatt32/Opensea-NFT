from datetime import date
from requests import request
from collection import Collection

API_KEY = 'XRcvi1wdOpza2JAdKVigSjL5fzXtwhEG'

class Asset:
    def __init__(self, json_data, slug, owner):
        # ASSET DETAILS
        self.name = json_data["name"]
        self.description = json_data["description"]
        self.token_id = json_data["token_id"]
        self.asset_url = json_data["permalink"]
        self.contract_address = json_data["asset_contract"]["address"]
        self.image_url = json_data["image_url"]
        self.slug = slug

        # COLLECTION DETAILS
        self.collection_name = json_data["collection"]["name"]
        self.collection_description = json_data["collection"]["description"]
        self.collection_slug = json_data["collection"]["slug"]
        self.verification_status = json_data["collection"]["safelist_request_status"]
        self.is_verified = json_data["collection"]["safelist_request_status"] == "verified"

        self.__ASSET_API_URL = f"https://api.opensea.io/api/v1/asset/{self.contract_address}/{self.token_id}"

    
        response = request("GET", self.__ASSET_API_URL)
        if response.status_code == 200:
            self.asset_json = response.json()
        else:
            self.asset_json = '' 
        self.collection = Collection(owner, slug)
        self.collection_count = self.collection.get_collection_count()        

    def get_token_name(self):
        token_name = {}
        token_name['collection_name'] = self.collection_name
        token_name['token_id'] = self.token_id
        token_name['name'] = self.name
        return token_name
    
    def get_usd(self, symbol):
        for token in self.asset_json['collection']['payment_tokens']:
            if (token['symbol']) == symbol:
                return token['usd_price']
    
    def purchase_to_usd(self, date, symbol):
        if symbol == 'WETH':
            symbol = 'ETH'
        url = f"https://api.polygon.io/v1/open-close/crypto/{symbol}/USD/{date}?adjusted=true&apiKey=XRcvi1wdOpza2JAdKVigSjL5fzXtwhEG"
        response = request('GET', (url)).json()
        return response['close']

    def get_price_purchased(self):
        asset_json = self.asset_json['last_sale']
        last_sale = {}
        try:
            symbol = asset_json['payment_token']['symbol']
            date = asset_json['event_timestamp'][:10]
            last_sale['symbol'] = symbol
            last_sale['date'] = date
            last_sale['decimals'] = int(asset_json['payment_token']['decimals'])
            last_sale['price'] = float(asset_json['total_price']) / (10 ** (last_sale['decimals']))
            last_sale['usd_price'] = last_sale['price'] * self.get_usd(last_sale['symbol'])
            #last_sale['usd_price'] = self.purchase_to_usd(last_sale['date'], last_sale['symbol'])
            return last_sale
        except:
            last_sale['symbol'] = 0
            last_sale['decimals'] = 0
            last_sale['price'] = 0
            last_sale['usd_price'] = 0
            last_sale['date'] = 0
            return last_sale

    def get_rarest_trait(self):
        asset_json = self.asset_json['traits']
        try:
            if len(asset_json) > 0:
                min = {
                    'count' : 100000
                }
                for trait in asset_json:
                    if (trait['trait_count'] < min['count'] and trait['trait_count'] > 0):
                        min['trait_type'] = trait['trait_type']
                        min['value'] = trait['value']
                        min['trait_count'] = int(trait['trait_count'])
            else:
                min = { 
                    'trait_type' : 'No traits listed',
                    'value' : 'No traits listed',
                    'trait_count' : 0
                }
        except:
            min = { 
                    'trait_type' : 'No traits listed',
                    'value' : 'No traits listed',
                    'trait_count' : 0
                }
        return min
    
    def get_trait_rarity(self, trait):
        trait_count = trait['trait_count']
        total_count = self.collection.get_collection_count()
        return {'trait_rarity_percentage' : trait_count / total_count}

    def get_current_calc_price(self):
        asset_json = self.asset_json['collection']
        current_price = {}
        try:
            current_price['symbol'] = asset_json['payment_tokens'][0]['symbol']
            if float(asset_json["stats"]["one_day_average_price"]) != 0:
                current_price['price'] = round(float(asset_json["stats"]["one_day_average_price"]), 3)
            elif float(asset_json["stats"]["seven_day_average_price"]) != 0:
                current_price['price'] = round(float(asset_json["stats"]["seven_day_average_price"]), 3)
            else:
                current_price['price'] = round(float(asset_json["stats"]["thirty_day_average_price"]), 3)
            try:
                rarity = self.get_trait_rarity(self.get_rarest_trait())['trait_rarity_percentage']
                multiplier = 1 + (.4 - rarity) 
                current_price['price'] = round(multiplier * current_price['price'], 3)
            except:
                pass
            current_price['usd_price'] = round(current_price['price'] * self.get_usd(current_price['symbol']), 2)
            return current_price
        except:
            current_price['symbol'] = 0
            current_price['price'] = 0
            current_price['usd_price'] = 0
            return current_price
