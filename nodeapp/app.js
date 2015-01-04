var Chain = require('chain-node');
var fs = require('fs');
var async = require('async');

var chain = new Chain({
  keyId: '146632b8b1ad98d188f41f139eb1299d',
  keySecret: 'c41d219707d1aba2909084223ac2fd37',
  blockChain: 'testnet3'
});

function Wallet(filename) {
    this.walletInfo = JSON.parse(fs.readFileSync(filename, 'utf8'));
    this.netcode = this.walletInfo['netcode'].toLowerCase();
    this.address = this.walletInfo[this.netcode + '_address_uncompressed'];
    this.wif = this.walletInfo['wif_uncompressed'];
    return this;
}

var wallet1 = new Wallet("../wallet1.json")

chain.getAddress(wallet1.address, function(err, resp) {
  console.log(resp);
});

var wallet2 = new Wallet("../wallet2.json")

chain.getAddress(wallet2.address, function(err, resp) {
  console.log(resp);
});

/*
 * Transaction code. needs from_address, from_secret, to_address, amount
async.waterfall([
    function(callback) {
        chain.buildTransaction(
            {
                inputs: [
                    {
                        address: wallet1.address,
                        // private_key: wallet1.wif
                    }
                ],
                outputs: [
                    {
                        address: wallet2.address,
                        amount: 0.01
                    }
                ]
            },
            callback
        );
    },
    function(resp, callback) {
        template = resp;
        private_keys = [wallet1.wif];
        signed_template = chain.signTemplate(template, private_keys);
        callback(null, signed_template);
    },
    function(signed_template, callback) {
        chain.sendTransaction(signed_template, callback);
    }
],
function(err, resp) {
    console.log(resp);
});

*/
