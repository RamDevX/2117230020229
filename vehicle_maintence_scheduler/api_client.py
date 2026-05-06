import requests

BASE_URL = "http://20.207.122.201/evaluation-service"

def fetch_depot(token):
    url = BASE_URL + "/depots"
    headers = {
        "Authorization": "Bearer " + token
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def fetch_vehicles(token):
    url = BASE_URL + "/vehicles"
    headers = {
        "Authorization": "Bearer " + token
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data