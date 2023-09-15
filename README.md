# Simple API for robyn
This repository is a simple API for [Robyn](https://github.com/facebookexperimental/Robyn/).

## Docker image
This respository is designed to assist in setting up an API for Robyn using [Plumber](https://www.rplumber.io/). The intention is to enable exchange of data more easily with other languages and improve workflows.

Enabling and running the API via docker allows the user to call certain Robyn functions using urls that are setup in the api. 

To run the docker locally use 

```
docker run -p 8000:8000 --name robyn-api arowley/robyn-api
```

## Docker hub
The docker container hosting the api is available on dockerhub.

```
docker pull arowley/robyn-api:latest
```
