"""

Author: D.Armstrong, 

GSQ. 26/04/2022

In the GSQ Open Data Portal, the QLD Goechemistry Exploration Database was divided into data blocks based on area, and uploaded as separate datasets.
# This streamlit app uses the API to extract geochem from an area based on a bounding box, and then uses the pyrolite package to analytes.

"""
from calendar import c
import streamlit as st
import requests
import json
from pyrolite.plot import pyroplot
from pyrolite.plot.density import density
from pyrolite.comp.codata import close
import os
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from pyrolite.util.plot.axes import share_axes
# import pandas_profiling
#from streamlit_pandas_profiling import st_profile_report

#########
# Layout
#########
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout="wide")
elements = ['Au','Au1','Cu','Pb','Zn','Ag','As','Bi','Mo','Mn','Fe','Ni','Co','Cr','V','Ba','Cd','Sn','Sb','Hg','Te','P','W','Zr','Ti','Mg','Th','U','Pt','Pd','S']

#########
# Title and Sidebar
#########

title_col1, title_col2 = st.columns([3, 22])
with title_col1:
       st.image("pyrolite.jpg", width=128)
with title_col2:
                st.title("Queensland Geochemistry with Pyrolite")
                st.write("The following app uses the GSQ Open Data Portal API to search for surface geochemistry datablocks within an area provided by a bounding box. Can then visualise and analyse the samples based on the Pyrolite pakcage.")
# Create a sidebar, to select surface sample type.
surface_type = st.sidebar.selectbox("Select Surface Sample",options = ['Rock Chip','Soil','Stream Sediment'])

surface_type_dict ={'Rock Chip':'s_rc','Soil':'s_so','Stream Sediment':'s_se'}
#########
# Data Extraction
#########
st.subheader("Data Extraction")

dw_col1, dw_col2 = st.columns([10,15])
with dw_col1:
        bbox = st.text_input(label = 'Enter bounding box coordinates to select an area', value ='141.7, -25, 144.2, -20.5')
        bbox = bbox.split(',')
        bbox = [float(x) for x in bbox]
        update_data = st.button("Extract Data")


#resource_dict = {}
#for k in os.listdir('./data/'):
#    resource_dict[k[0:4]] = k
#    df = pd.read_csv('./data/'+k)
#    df =df.rename(columns={"Latitude":"latitude",'Longitude':"longitude"})
def api_call(bbox):
    api = 'https://geoscience.data.qld.gov.au/api/action/'
    # Search using bounding box provided, and filter the query (fq) to reports only
    response = requests.get(api + 'package_search'+'?rows=1000&start=0',
                   params={
                       'ext_bbox':bbox,
                       'fq':[
                           'type:geochemistry'
                       ]
                   })

    df_list = []
    for k in response.json()['result']['results']:
        for file in k['resources']:
            print(file['name'])
            if file['format'].lower() == 'csv' and file['name'][0:4].lower() == 's_rc':
                df = pd.read_csv(file['url'])
                df_list.append(df)
    final = pd.concat(df_list)
    final =final.rename(columns={"Latitude":"latitude",'Longitude':"longitude"})
    return(final)

if 'df' not in st.session_state:
	st.session_state.df = []

if update_data:
    st.session_state.df = api_call(bbox)

if len(st.session_state.df)>0:
    
    with dw_col1:
        st.write(st.session_state.df)
    #    pr = df.profile_report()
    #    st_profile_report(pr)
    with dw_col2:
        st.map(st.session_state.df[['latitude','longitude']])
    
col1, col2 = st.columns(2)
col1.subheader("Ternary Plots")
ternary_elements = col1.multiselect("Select three elements for ternary plots",elements)
if col1.button("Produce Ternary Plots"):
        fig, ax = plt.subplots()
        ax = st.session_state.df.loc[:, ternary_elements].pyroplot.scatter(c="b")
        col1.pyplot()

st.subheader("HeatScatter Plots")
bivar = st.multiselect("Select bivariate elements",elements)
trivar = st.multiselect("Select trivariate elements",elements)
if st.button("Produce Heatscatter Plots"):
    fig, ax = plt.subplots(3, 4, figsize=(18, 15))

    ax = ax.flat
    share_axes(ax[:4], which="xy")
    share_axes(ax[4:8], which="xy")
    share_axes(ax[8:], which="xy")

    contours = [0.95, 0.66, 0.3]
    # linear-scaled comparison
    st.session_state.df.loc[:, bivar].pyroplot.scatter(ax=ax[0], c="k", s=10, alpha=0.3)
    st.session_state.df.loc[:, bivar].pyroplot.density(ax=ax[1])
    st.session_state.df.loc[:, bivar].pyroplot.density(ax=ax[2], contours=contours)
    st.session_state.df.loc[:, bivar].pyroplot.heatscatter(ax=ax[3], s=10, alpha=0.3)
    # log-log plots
    st.session_state.df.loc[:, bivar].pyroplot.scatter(ax=ax[4], c="k", s=10, alpha=0.3)
    st.session_state.df.loc[:, bivar].pyroplot.density(ax=ax[5], logx=True, logy=True)
    st.session_state.df.loc[:, bivar].pyroplot.density(ax=ax[6], contours=contours, logx=True, logy=True)
    st.session_state.df.loc[:, bivar].pyroplot.heatscatter(ax=ax[7], s=10, alpha=0.3, logx=True, logy=True)
    # ternary plots
    st.session_state.df.loc[:, trivar].pyroplot.scatter(ax=ax[8], c="k", s=10, alpha=0.1)
    st.session_state.df.loc[:, trivar].pyroplot.density(ax=ax[9], bins=100)
    st.session_state.df.loc[:, trivar].pyroplot.density(ax=ax[10], contours=contours, bins=100)
    st.session_state.df.loc[:, trivar].pyroplot.heatscatter(ax=ax[11], s=10, alpha=0.3, renorm=True)
    fig.subplots_adjust(hspace=0.4, wspace=0.4)

    titles = ["Scatter", "Density", "Contours", "Heatscatter"]
    for t, a in zip(titles + [i + " (log-log)" for i in titles], ax):
        a.set_title(t)
    #plt.tight_layout()
    st.pyplot()