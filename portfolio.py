from streamlit.elements.image import MAXIMUM_CONTENT_WIDTH
from asset import Asset
import requests


class Portfolio:
    def __init__(self, owner):
        params = {
            'owner' : owner
        }
        r = requests.get('https://api.opensea.io/api/v1/assets', params = params)
        response = r.json()['assets']
        self.asset_list = []
        for asset in response:
            asset_slug = asset['collection']['slug']
            self.asset_list.append(Asset(asset, asset_slug, owner))
        self.username = self.asset_list[0].asset_json['owner']['user']['username']
            
    
    def get_num_assets(self):
        return len(self.asset_list)

    def financial_summary(self):
        financials = {
            'current_value_usd' : 0.0,
            'cost_basis_usd' : 0.0
        }
        for asset in self.asset_list:
            if asset.get_price_purchased()['usd_price'] == None:
                pass
            else:
                financials['cost_basis_usd'] += asset.get_price_purchased()['usd_price']
                financials['current_value_usd'] += asset.get_current_calc_price()['usd_price']
        return financials

def profit_loss(value, cost_basis):
    p_and_l = {
        "usd" : value - cost_basis,
        "percent" : (value - cost_basis) / cost_basis
    }
    return p_and_l




