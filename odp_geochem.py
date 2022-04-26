"""

Author: D.Armstrong, 

GSQ. 26/04/2022

In the GSQ Open Data Portal, the QLD Goechemistry Exploration Database was divided into data blocks based on area, and uploaded as separate datasets.
# This streamlit app uses the API to extract geochem from an area based on a bounding box, and then uses the pyrolite package to analytes.

"""

import streamlit as st
import requests
import json
# Add a Title
st.set_page_config(layout="wide")

#%%
#st.image("./preview.jpg", width=600)
st.title("GSQ Geochemistry and Pyrolite")
st.write("The following app uses the GSQ Open Data Portal API to search for surface geochemistry datablocks within an area provided by a bounding box. Can then visualise and analyse the samples based on the Pyrolite pakcage.")
# Create a sidebar, to select surface sample type.
st.sidebar.selectbox("Select Surface Sample",options = ['Soil','Stream Sediment','Rockhip'])

#bbox = [148.7, -26.6, 148.9, -26.5]
bbox = st.text_input(label = 'Enter bounding box coordinates to select an area', value ='148.7, -26.6, 148.9, -26.5')
bbox = bbox.split(',')
bbox = [float(x) for x in bbox]
bbox = [140.7, -28.6, 148.9, -26.5]
st.write(bbox)
#update_data = st.button("Extract Data")
#%%
bbox = [140.7, -28.6, 148.9, -26.5]
api = 'https://geoscience.data.qld.gov.au/api/action/'
# Search using bounding box provided, and filter the query (fq) to reports only
response = requests.get(api + 'package_search',
                   params={
                    #'ext_bbox':bbox,
                       'fq':[
                           'type:geochemistry'
                       ]
                   })
# Show dataset count
st.write(response.json()['result']['count'])


# %%
