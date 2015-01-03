from __future__ import print_function
import requests, json

from pycoin.convention import btc_to_satoshi
from pycoin.tx import Tx, Spendable
from pycoin.tx.tx_utils import create_tx, sign_tx, create_signed_tx
from pycoin.serialize import h2b
from pycoin import encoding

NETWORK = 'testnet3'

API_URL = 'api.chain.com/v2/'

API_KEY = "146632b8b1ad98d188f41f139eb1299d"
API_KEY_SECRET = "c41d219707d1aba2909084223ac2fd37"

def make_request_url(method, *params):
    url_format = 'https://{}:{}@' + API_URL + '{}/{}/{}'
    param_string = '/'.join(params)
    url_string = url_format.format(API_KEY, API_KEY_SECRET, NETWORK, method, param_string)
    return url_string

def spendables_for_address(bitcoin_address):
    """
    Return a list of Spendable objects for the
    given bitcoin address.
    """
    response = requests.get(make_request_url('addresses', bitcoin_address, 'unspents'))
    r = response.json()
    spendables = []
    for u in r:
        previous_hash = h2b(u.get("transaction_hash"))
        previous_index = u.get("output_index")
        coin_value = u.get("value")
        script = h2b(u.get("script_hex"))
        spendables.append(Spendable(coin_value, script, previous_hash, previous_index))
    return spendables

class Wallet:
    def __init__(self, filename):
        self.wallet_info = json.load(open(filename))
        self.netcode = self.wallet_info['netcode'].lower()
        self.address = self.wallet_info[self.netcode + '_address_uncompressed']
        self.wif = self.wallet_info['wif_uncompressed']
        self.secret_exponent_db = {}
        public_pair = [int(self.wallet_info['public_pair_x']),
                int(self.wallet_info['public_pair_y'])]
        hash160 = encoding.public_pair_to_hash160_sec(public_pair, compressed=False)
        self.secret_exponent_db[hash160] = (int(self.wallet_info['secret_exponent']),
                public_pair,
                False)


wallet1 = Wallet('wallet1.json')
wallet2 = Wallet('wallet2.json')

url = make_request_url('addresses', wallet1.address)
response = requests.get(url)
print(response.content)

url = make_request_url('addresses', wallet2.address)
response = requests.get(url)
print(response.content)

spendables = spendables_for_address(wallet1.address)
for i in spendables:
    print(i)
# tx = create_tx(spendables=spendables,
#                payables=[(wallet2.address, btc_to_satoshi(1))],
#                fee=0)
# sign_tx(tx, wifs=[wallet1.wif], secret_exponent_db=wallet1.secret_exponent_db)

tx = create_signed_tx(spendables=spendables,
               payables=[(wallet2.address, 10000)],
               wifs=[wallet1.wif], secret_exponent_db=wallet1.secret_exponent_db,
               fee=0)
tx_payload = {'signed_hex': tx.id()}
print(tx.id())
headers = {'content-type':'application/json'}
url = make_request_url('transactions', 'send')
print(url)
response = requests.post(url, data=json.dumps(tx_payload), headers=headers)
print(response.json())

