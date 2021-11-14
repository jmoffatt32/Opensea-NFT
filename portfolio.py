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

    def portfolio_value_usd(self):
        usd_value = 0.0
        for asset in self.asset_list:
            if asset.get_current_price()['usd_price'] != None:
                usd_value += asset.get_current_price()['usd_price']
            else:
                pass
        return usd_value
    
    def cost_basis_usd(self):
        usd_value = 0.0
        for asset in self.asset_list:
            if asset.get_price_purchased()['usd_price'] != None:
                usd_value += asset.get_price_purchased()['usd_price']
            else:
                pass
        return usd_value

    def financial_summary(self):
        financials = {
            'current_value_usd' : 0.0,
            'cost_basis_usd' : 0.0
        }
        for asset in self.asset_list:
            if asset.get_price_purchased()['usd_price'] != None:
                financials['cost_basis_usd'] += asset.get_price_purchased()['usd_price']
            else:
                pass
            if asset.get_current_price()['usd_price'] != None:
                financials['current_value_usd'] += asset.get_current_price()['usd_price']
            else:
                pass
        #financials["profit_loss_usd"] = financials['current_value_usd'] - financials['cost_basis_usd']
        #financials['profit_loss_percent'] = financials['profit_loss_usd'] / financials['cost_basis_usd']
        return financials
