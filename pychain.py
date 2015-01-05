from __future__ import print_function
import requests, json


NETWORK = 'testnet3'
API_URL = 'api.chain.com/v2/'
API_KEY = "146632b8b1ad98d188f41f139eb1299d"
API_KEY_SECRET = "c41d219707d1aba2909084223ac2fd37"

def make_request_url(method, *params):
    url_format = 'https://{}:{}@' + API_URL + '{}/{}/{}'
    param_string = '/'.join(params)
    url_string = url_format.format(API_KEY, API_KEY_SECRET, NETWORK, method, param_string)
    return url_string

def getBalance(addr):
    url = make_request_url('addresses', addr)
    response = requests.get(url)
    reqdic = response.json()[0]
    return reqdic["confirmed"],reqdic["total"] 
