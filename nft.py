import requests
import streamlit as st
from asset import Asset
from portfolio import Portfolio
from collection import Collection
import collection

#sidebar
owner = st.sidebar.text_input('Owner', key = 1)

#header
st.header("Open Sea NFT API Explorer")

#query params
params = {}
if owner: 
    params['owner'] = owner

#body
if not owner:
    pass
else:
    owner_portfolio = Portfolio(owner)
    mekaverse_collection = Collection(owner, 'mekaverse')

    st.header(f"{owner_portfolio.username}'s Portfolio:")
 
    st.write(f"Value: ${round(owner_portfolio.financial_summary()['current_value_usd'], 2)} USD")
    #st.write(f"P/L ($): ${round(owner_portfolio.financial_summary()['profit_loss_usd'], 2)} USD")
    #st.write(f"P/L (%): {round(owner_portfolio.financial_summary()['profit_loss_percent'], 4) * 100}%")
    
    st.header("Assets:")
    i = 1
    for asset in owner_portfolio.asset_list:
        i += 1
        st.subheader(f"Collection: {asset.get_token_name()['collection_name']}")
        st.write(f"Token ID: {asset.get_token_name()['token_id']}")
        st.write(f"Name: {asset.get_token_name()['name']}")
        #st.write(f"Slug: {asset.slug} - (Collection size: {int(asset.collection_count)})")
        
        st.write(asset.asset_url)
        st.image(asset.image_url)
       
        #st.write(f"Floor Price: {asset.get_floor_price()['price']} {asset.get_floor_price()['symbol']} (${asset.get_floor_price()['usd_price']} USD)")
        #st.write(f"Current Price: {asset.get_current_price()['price']} {asset.get_current_price()['symbol']} (${asset.get_current_price()['usd_price']} USD)")
        #st.write(f"Average Price: {asset.get_average_price()['price']} {asset.get_average_price()['symbol']} (${asset.get_average_price()['usd_price']} USD)")
        st.write(f"Calculated Current Sale Price: {asset.get_current_calc_price()['price']} {asset.get_current_calc_price()['symbol']} (${asset.get_current_calc_price()['usd_price']} USD)")
        if (type(asset.get_price_purchased()['price']) == float):
            st.write(f"Price Purchased: {asset.get_price_purchased()['price']} {asset.get_price_purchased()['symbol']} (${asset.get_price_purchased()['usd_price']} USD)")
        else:
            price_purchased = st.text_input("Price Purchased (USD)", key = i)
            if price_purchased != 0:
                st.write(f"Price Purchased: ${price_purchased} USD")
        if asset.get_rarest_trait()['trait_count'] != 0:
            st.write(f"Rarest Trait: {asset.get_rarest_trait()['trait_type']} - {asset.get_rarest_trait()['value']}  ||  Count: {asset.get_rarest_trait()['trait_count']}  ||  {round((asset.get_trait_rarity(asset.get_rarest_trait())['trait_rarity_percentage']) * 100, 2)}%")
            #st.write(f"\tCount: {asset.get_rarest_trait()['trait_count']}")
            #st.write(f"{round((asset.get_trait_rarity(asset.get_rarest_trait())['trait_rarity_percentage']) * 100, 2)}%" )
        else: 
            st.write("No traits available")



    st.subheader("Asset JSON:")
    st.write(owner_portfolio.asset_list[5].asset_json)
