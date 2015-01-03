from __future__ import print_function
import requests, json

from pycoin.convention import btc_to_satoshi
from pycoin.tx import Tx, Spendable
from pycoin.tx.tx_utils import create_tx, sign_tx, create_signed_tx
from pycoin.serialize import h2b
from pycoin import encoding

NETWORK = 'BTCTEST'

API_URL = 'https://chain.so/api/v2/'

def make_request_url(method, *params):
    url_format = API_URL + '{}/{}/{}'
    param_string = '/'.join(params)
    url_string = url_format.format(method, NETWORK, param_string)
    return url_string

def spendables_for_address(bitcoin_address):
    """
    Return a list of Spendable objects for the
    given bitcoin address.
    """
    response = requests.get(make_request_url('get_tx_unspent', bitcoin_address))
    r = response.json()
    spendables = []
    for u in r.get("data", {}).get("txs", []):
        coin_value = btc_to_satoshi(u.get("value"))
        script = h2b(u.get("script_hex"))
        previous_hash = h2b(u.get("txid"))
        previous_index = u.get("output_no")
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

response = requests.get(make_request_url('get_address_balance', wallet1.address))

print(response.json())
response = requests.get(make_request_url('get_address_balance', wallet2.address))

print(response.json())

spendables = spendables_for_address(wallet1.address)
for i in spendables:
    print(i)
# tx = create_tx(spendables=spendables,
#                payables=[(wallet2.address, btc_to_satoshi(1))],
#                fee=0)
# sign_tx(tx, wifs=[wallet1.wif], secret_exponent_db=wallet1.secret_exponent_db)

tx = create_signed_tx(spendables=spendables,
               payables=[(wallet2.address, btc_to_satoshi(1))],
               wifs=[wallet1.wif], secret_exponent_db=wallet1.secret_exponent_db,
               fee=0)
tx_payload = {'tx_hex': tx.id()}
headers = {'content-type':'application/json'}
response = requests.post(make_request_url('send_tx'), data=json.dumps(tx_payload), headers=headers)
print(response.json())

