# Simple API for robyn
This repository is a proof of concept of a simple API for [Robyn](https://github.com/facebookexperimental/Robyn/).

## Overview
This respository is a proof of concept of a relatively simple API for Robyn set up using [Plumber](https://www.rplumber.io/). The api is intended to run within a docker container. The intention is to enable exchange of data more easily with other languages and improve workflows while working with Robyn. Enabling and running the API via docker allows the user to call certain Robyn functions using urls that are setup in the api without installing R or Robyn itself in the host system. 

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

As this is is a proof of concept, only the following endpoints are enabled.

<table>
    <thead>
        <tr>
            <th>Endpoint</th>
            <th>Purpose</th>
            <th>Arguments</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=5>/robynrun</td>
            <td rowspan=5>Collects a robyn input from json, and executes robyn run. Optionally returns one pagers.</td>
            <td>modelData - Serialized dataframe, serialize this in a manner similar to the python example (dataframe -> featherfile -> hexstring)</td>
        </tr>
        <tr>
            <td>jsonInput - Additional parameters for robyninputs in json format</td>
        <tr>
        <tr>
            <td>jsonRunArgs - Additional parameters for robynrun in json format</td>
        </tr>
        <tr>
            <td>onePagers - Boolean - Whether to build the one pager files for models</td>
        </tr>
        <tr>
            <td>/dt_prophet_holiday</td>            
            <td>Returns Robyn prophet holidays dataset</td>
            <td>None</td>
        </tr>
        <tr>
            <td>/dt_simulted_weekly</td>
            <td>Returns Robyn simulated demand dataset</td>
            <td>None</td>
        </tr>
    </tbody>
</table>

## Docker hub
The docker container hosting the api is available on dockerhub.

```
docker pull arowley/robyn-api:latest
```

It can also be built from within the docker folder. 
