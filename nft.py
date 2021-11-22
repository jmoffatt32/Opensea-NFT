import requests
import streamlit as st
from asset import Asset
from portfolio import Portfolio, profit_loss
from collection import Collection
import time


#sidebar
st.sidebar.subheader("[Survey Link](https://docs.google.com/forms/d/e/1FAIpQLSfRmkQUYHYCWBgIDRnvX1gjg_mM5aTxkAm0rbYFS_rLTgUW0A/viewform?usp=sf_link)")
owner = st.sidebar.text_input('Owner (Wallet Address)', key = 1)

#header
st.header("DeFi-Able")

#query params
params = {}
if owner: 
    params['owner'] = owner
percent_complete = 0
#body
if not owner:
    st.subheader("Some addresses to try:")
    st.markdown("**(Copy and paste into owner field in the sidebar)**")
    st.write("0x0864224f3cc570ab909ebf619f7583ef4a50b826")
    st.write("0xca8b73101e12c03e4e9eacf0e180fc10edf859e2")
    st.write("0x6a83d1a68fb09c28b3c70d37b458231ad3f0ec71")
else:
    owner_portfolio = Portfolio(owner)
    mekaverse_collection = Collection(owner, 'mekaverse')

    cost_basis = 0.0
    st.header(f"{owner_portfolio.username}'s Portfolio:")

    st.header("Assets:")
    i = 1
    f = 0
    #my_bar = st.progress(percent_complete)
    for asset in owner_portfolio.asset_list:
        i += 1
        #my_bar.progress(percent_complete + i)
        st.subheader(f"Collection: {asset.get_token_name()['collection_name']}")
        st.write(f"Token ID: {asset.get_token_name()['token_id']}")
        st.write(f"Name: {asset.get_token_name()['name']}")
        
        st.write(asset.asset_url)
        st.image(asset.image_url)
        with st.expander("See Details:"):
            
            #current sale price
            if asset.get_current_calc_price()['price'] == None:
                st.markdown("Calculated Current Sale Price: **Necessary Data Not Provided by OpenSea**")
            else:
                st.write(f"Calculated Current Sale Price: **{asset.get_current_calc_price()['price']} {asset.get_current_calc_price()['symbol']} (${asset.get_current_calc_price()['usd_price']} USD)**")
            
            #price purchased
            if (type(asset.get_price_purchased()['price']) == float):
                st.write(f"Price Purchased: **{asset.get_price_purchased()['price']} {asset.get_price_purchased()['symbol']} (${asset.get_price_purchased()['usd_price']} USD)**")
                cost_basis += asset.get_price_purchased()['usd_price']
                f += 1
            else:
                flag = True
                with st.form(f"{i}"):
                    price_purchased = st.text_input("Price Purchased (USD)", key = i)
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        f += 1
                        st.write(f"Price Purchased: **${price_purchased} USD**")
                        cost_basis += int(price_purchased)
            try:
                if asset.get_rarest_trait()['trait_count'] != 0:
                    st.write(f"Rarest Trait: {asset.get_rarest_trait()['trait_type']} - {asset.get_rarest_trait()['value']}  ||  Count: **{asset.get_rarest_trait()['trait_count']}**  ||  **{round((asset.get_trait_rarity(asset.get_rarest_trait())['trait_rarity_percentage']) * 100, 2)}%**")
                else: 
                    st.write("No Token Traits")
            except:
                st.write("No Token Traits")

    st.sidebar.subheader("Portfolio Details:")
    value = round(owner_portfolio.financial_summary()['current_value_usd'], 2)
    cost = round(owner_portfolio.financial_summary()['cost_basis_usd'], 2)
    st.sidebar.markdown(f"Value: **${value} USD**")
    st.sidebar.markdown(f"Cost Basis: **${cost} USD**")
    st.sidebar.markdown(f"P/L: **${profit_loss(value, cost)['usd']} USD**")
    st.sidebar.markdown(f"P/L: **{round(profit_loss(value, cost)['percent'] * 100, 2)}%**")
    st.sidebar.markdown(f"Number of Assets: **{len(owner_portfolio.asset_list)}**")

#st.write(owner_portfolio.asset_list[0].collection.response_json)
# purchase_json = owner_portfolio.asset_list[3].get_price_purchased()
# st.write(purchase_json)
# st.write(owner_portfolio.asset_list[3].purchase_to_usd(purchase_json['date'], purchase_json['symbol']))
