import requests
import streamlit as st
from asset import Asset
from portfolio import Portfolio
from collection import Collection


#sidebar
owner = st.sidebar.text_input('Owner (Wallet Address)', key = 1)

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
    st.markdown(f"Value: **${round(owner_portfolio.financial_summary()['current_value_usd'], 2)} USD**")

    st.header("Assets:")
    i = 1
    for asset in owner_portfolio.asset_list:
        i += 1
        st.subheader(f"Collection: {asset.get_token_name()['collection_name']}")
        st.write(f"Token ID: {asset.get_token_name()['token_id']}")
        st.write(f"Name: {asset.get_token_name()['name']}")
        
        st.write(asset.asset_url)
        st.image(asset.image_url)
        with st.expander("See Details:"):
            st.write(f"Calculated Current Sale Price: **{asset.get_current_calc_price()['price']} {asset.get_current_calc_price()['symbol']} (${asset.get_current_calc_price()['usd_price']} USD)**")
            if (type(asset.get_price_purchased()['price']) == float):
                st.write(f"Price Purchased: **{asset.get_price_purchased()['price']} {asset.get_price_purchased()['symbol']} (${asset.get_price_purchased()['usd_price']} USD)**")
            else:
                with st.form(f"{i}"):
                    price_purchased = st.text_input("Price Purchased (USD)", key = i)
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        st.write(f"Price Purchased: **${price_purchased} USD**")
            try:
                if asset.get_rarest_trait()['trait_count'] != 0:
                    st.write(f"Rarest Trait: {asset.get_rarest_trait()['trait_type']} - {asset.get_rarest_trait()['value']}  ||  Count: **{asset.get_rarest_trait()['trait_count']}**  ||  **{round((asset.get_trait_rarity(asset.get_rarest_trait())['trait_rarity_percentage']) * 100, 2)}%**")
                else: 
                    st.write("No traits available")
            except:
                st.write("No traits available")


