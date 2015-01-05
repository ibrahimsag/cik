var Chain = require('chain-node');
var fs = require('fs');
var async = require('async');

var chain = new Chain({
  keyId: '146632b8b1ad98d188f41f139eb1299d',
  keySecret: 'c41d219707d1aba2909084223ac2fd37',
  blockChain: 'testnet3'
});

var args = process.argv.slice(2);

function Wallet(filename) {
    this.walletInfo = JSON.parse(fs.readFileSync(filename, 'utf8'));
    this.netcode = this.walletInfo['netcode'].toLowerCase();
    this.address = this.walletInfo[this.netcode + '_address_uncompressed'];
    this.wif = this.walletInfo['wif_uncompressed'];
    return this;
}

/*
var wallet1 = new Wallet("../wallet1.json")
var wallet2 = new Wallet("../wallet2.json")

console.log(wallet1.address, wallet1.wif, wallet2.address);

chain.getAddress(wallet1.address, function(err, resp) {
  console.log(resp);
});

chain.getAddress(wallet2.address, function(err, resp) {
  console.log(resp);
});
*/

/*
 * Transaction transacted here.
 */
input_address = args[0];
input_secret = args[1];
output_address = args[2];
amount = args[3];
async.waterfall([
    function(callback) {
        chain.buildTransaction(
            {
                inputs: [
                    {
                        address: input_address,
                    }
                ],
                outputs: [
                    {
                        address: output_address,
                        amount: amount
                    }
                ]
            },
            callback
        );
    },
    function(resp, callback) {
        template = resp;
        if(template.message) {
            callback(template, null);
        }
        private_keys = [input_secret];
        signed_template = chain.signTemplate(template, private_keys);
        callback(null, signed_template);
    },
    function(signed_template, callback) {
        chain.sendTransaction(signed_template, callback);
    }
],
function(err, resp) {
    if(err || resp.message) {
        if(err)
            console.log(err);
        if(resp)
            console.log(resp);
        process.exit(1);
    }
    console.log(resp);
});
