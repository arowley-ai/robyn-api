import requests
import json
import datetime as dt
import binascii
import io
import pandas as pd
import os

from PIL import Image

Image.MAX_IMAGE_PIXELS = 2**30

inputArgs = {
    "InputCollect" : {
        "date_var": "DATE",
        "dep_var": "revenue",
        "dep_var_type": "revenue",
        "prophet_vars": ["trend", "season", "holiday"],
        "prophet_country": "DE",
        "context_vars" : ["competitor_sales_B", "events"],
        "paid_media_spends": ["tv_S", "ooh_S", "print_S", "facebook_S", "search_S"],
        "organic_vars" : "newsletter",
        "window_start": "2016-01-01",
        "window_end": "2018-12-31",
        "adstock": "geometric",
        "hyperparameters": {
          "facebook_S_alphas" : [0.5, 3],
          "facebook_S_gammas" : [0.3, 1],
          "facebook_S_thetas" : [0, 0.3],
          "print_S_alphas" : [0.5, 3],
          "print_S_gammas" : [0.3, 1],
          "print_S_thetas" : [0.1, 0.4],
          "tv_S_alphas" : [0.5, 3],
          "tv_S_gammas" : [0.3, 1],
          "tv_S_thetas" : [0.3, 0.8],
          "search_S_alphas" : [0.5, 3],
          "search_S_gammas" : [0.3, 1],
          "search_S_thetas" : [0, 0.3],
          "ooh_S_alphas" : [0.5, 3],
          "ooh_S_gammas" : [0.3, 1],
          "ooh_S_thetas" : [0.1, 0.4],
          "newsletter_alphas" : [0.5, 3],
          "newsletter_gammas" : [0.3, 1],
          "newsletter_thetas" : [0.1, 0.4],
          "train_size": [0.5, 0.8]
        }
    },
    "OutputCollect": {
        "conv_msg": []
    }
}

runArgs = {
    "iterations" : 200,
    "trials" : 5, 
    "ts_validation" : True,
    "add_penalty_factor" : False,
    "seed" : 123
}

apiBaseUrl = "http://localhost:8000/{}"

hexToPng = lambda fileName, hexData: Image.open(io.BytesIO(binascii.unhexlify(hexData))).save(fileName, "png")
dateConv = lambda date: dt.datetime.strptime(date, '%Y-%m-%d').date()

def asSerialisedFeather(modelData):
    modelDataFeather = io.BytesIO()
    pd.DataFrame(modelData).to_feather(modelDataFeather)
    modelDataFeather.seek(0)
    modelDataBinary = modelDataFeather.read()
    return binascii.hexlify(modelDataBinary).decode()

# Get the sample dataset from Robyn api for use in later steps
response = requests.post(apiBaseUrl.format('dt_simulated_weekly'))
respJson = json.loads(response.content.decode('utf-8'))
dtSimulatedWeekly = [{'DATE' : dateConv(rec['DATE']),**{col:rec[col]for col in rec if col!='DATE'}} for rec in respJson]
dtSimulatedWeeklyDf = pd.DataFrame(dtSimulatedWeekly)

# Build the payload for the robyn run
payload = {
    'modelData' : asSerialisedFeather(dtSimulatedWeeklyDf), # Substitute your own data here
    'jsonInput' : json.dumps(inputArgs),
    'jsonRunArgs' : json.dumps(runArgs),
    'onePagers' : True # Causes the api to generate all one pagers for the cluster selected models
}

# Get response
response = requests.post(apiBaseUrl.format('robynrun'),data=payload)
respJson = json.loads(response.content.decode('utf-8'))

# Make directory for output
if not os.path.exists('./output'):
    os.makedirs('./output')
    
# Optionally dump the entire contents of response to disk
with open("output/outfile.json", "w") as outfile:
    outfile.write(json.dumps(respJson, indent=4))

# Optionally dump the model one pagers into a directory
if payload['onePagers']:
    for result in respJson['clusters']['models']:
        for model in result['onepagers']:
            hexToPng('./output/{0}.png'.format(model),result['onepagers'][model][0])
