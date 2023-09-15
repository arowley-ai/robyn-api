# Simple API for robyn
This repository is a simple API for [Robyn](https://github.com/facebookexperimental/Robyn/).

## Docker image
This respository is designed to assist in setting up an API for Robyn using [Plumber](https://www.rplumber.io/). The intention is to enable exchange of data more easily with other languages and improve workflows. Enabling and running the API via docker allows the user to call certain Robyn functions using urls that are setup in the api. 

## Usage

To run the docker container locally use:

```
docker run -p 8000:8000 --name robyn-api arowley/robyn-api
```

To run the example script in Python use:
```
pip install -r requirements.txt
```
and
```
python python-minimal.py
```
If you are running the docker container remotely, you may need to update the base url for the api, amend:
```
apiBaseUrl = "http://localhost:8000/{}"
```

## End points

Only the following endpoints are enabled
- /dt_simulated_weekly - no arguments
- /dt_prophet_holidays - no arguments
- /robynrun - arguments are
  - modelData - Serialized dataframe, serialize this in a manner similar to the python example (dataframe -> featherfile -> hexstring)
  - jsonInput - Additional parameters for robyninputs in json format
  - jsonRunArgs - Additional parameters for robynrun in json format
  - onePagers - Boolean - Whether to build the one pager files for models


## Serialising

## Docker hub
The docker container hosting the api is available on dockerhub.

```
docker pull arowley/robyn-api:latest
```
