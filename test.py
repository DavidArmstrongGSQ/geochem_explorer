
#%%
import requests
import json
import pandas as pd
#%%
bbox= [140.7, -30.6, 148.9, -26.5]
api = 'https://geoscience.data.qld.gov.au/api/action/'
# Search using bounding box provided, and filter the query (fq) to reports only
response = requests.get(api + 'package_search'+'?rows=1000&start=0',
                   params={
                       'ext_bbox':bbox,
                       'fq':[
                           'type:geochemistry'
                       ]
                   })

#%%
df_list = []
for k in response.json()['result']['results']:
    for file in k['resources']:
        print(file['name'])
        if file['format'].lower() == 'csv' and file['name'][0:4].lower() == 'h_lo':
            df = pd.read_csv(file['url'])
            df_list.append(df)
final = pd.concat(df_list)
# %%
