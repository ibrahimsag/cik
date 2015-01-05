#! /usr/bin/env python
"""cik.
USAGE:
	cik.py send ([-]| --recv=<receiver_wallet_address> --amount=<amount_to_be_sent>)
	cik.py init ( --new | [-] | --addr=<wallet_address> --pwd=<wallet_password>)
	cik.py reset
	cik.py status ( --addr=<wallet_address | [-] )
	cik.py (-h | --help)
	cik.py --version
Options:
  -h --help  	Show this screen.
  --version  		Show version.
"""
cik_version = 0.3
from docopt import docopt
import ConfigParser
import getpass
import pychain
import subprocess
import json

W_ADDR = ""
W_PWD = ""
W_WIF_UNCOMP = ""

def init(addr, pwd, config):
	"Set addr and pwd as wallet address and wallet secret"
	config.set("user_info", "wallet.address", addr)
	config.set("user_info", "wallet.password", pwd)
	wif = subprocess.Popen("ku -uW " + pwd, shell=True, stdout=subprocess.PIPE).stdout.read()
	config.set("user_info", "wallet.wif", wif)
	with open("conf.cfg",'w') as cfgfile:
		config.write(cfgfile)
		print "Config file update successful"
	return

def printStatus(addr=""):
	"Get wallet address and baalance"
	if not addr:
		if not W_ADDR:
			print "Address/Password is not set, please set these values by running:"
			print"\tcik.py init --addr=<wallet_address> --pwd=<wallet_password>"
			print "\tor"
			print"\tcik.py init -"
			return
		else:
			addr = W_ADDR
	#TODO: query [module] to get current balance
	print "Address:\t%s"%addr
	confirmed_dic,total_dic = pychain.getBalance(addr)
	pending = total_dic['balance'] - confirmed_dic['balance']
	absolute = confirmed_dic['balance']
	print "Balance: {0} \t Pending: {1}".format(absolute, pending)

	return

def reset():
	"Clear Account info from local config file"
	config.set("user_info", "wallet.address", "")
	config.set("user_info", "wallet.password", "")
	with  open("conf.cfg",'w') as cfgfile:
		config.write(cfgfile)
		print "Reset successful"
	return

def send(recv, amount):
	"Sends amount to recv(addr) from local wallet address"
	res = subprocess.Popen("node ./nodeapp/app.js %s %s %s %d"%(W_ADDR, W_WIF_UNCOMP, recv, int(amount)), shell=True, stdout=subprocess.PIPE).stdout.read()
	#TODO: call [module] to construct, sign and send transaction message
	print "node ./nodeapp/app.js %s %s %s %d"%(W_ADDR, W_WIF_UNCOMP, recv, int(amount))
	print res
	return

def generate():
	wallet = subprocess.Popen("ku create -n XTN -w -j", shell=True, stdout=subprocess.PIPE).stdout.read()
	wallet_j = json.loads(wallet)
	print "Wallet generated ..."
	init(wallet_j['xtn_address_uncompressed'],wallet_j['wallet_key'],config)


if __name__ == '__main__':
	#TODO Read cnf file
	arguments = docopt(__doc__,help=True, version=cik_version)
	config = ConfigParser.ConfigParser()
	config.read('conf.cfg')
	W_ADDR = config.get('user_info', 'wallet.address')
	W_PWD = config.get('user_info', 'wallet.password')
	W_WIF_UNCOMP = config.get('user_info', 'wallet.wif')
	print(arguments)
	if arguments['init']:
		if arguments['--new']:
			generate()
		elif arguments['--addr'] and arguments['--pwd']:
			init(arguments['--addr'], arguments['--pwd'], config)
		else:
			init(raw_input("Your wallet address:"), getpass.getpass("Your wallet password:"), config)
	elif arguments['send']:
		if arguments['--recv'] and arguments['--amount']:
			send(arguments['--recv'],arguments['--amount'])
		else:
			send(raw_input(" Please specify the receiver:\t"), raw_input("How much do you want to send:\t"))
	elif arguments['status']:
		if arguments["--addr"]:
			printStatus(arguments["--addr"])
		else:
			printStatus()
	elif arguments['reset']:
		reset()
	elif arguments['--version']:
		print "cik Version %f"%cik_version
