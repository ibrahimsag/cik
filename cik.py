#! /usr/bin/env python
"""cik.
USAGE:
	cik.py send ([-]| --recv=<receiver_wallet_address> --amount=<amount_to_be_sent>)
	cik.py init ([-]| --addr=<wallet_address> --pwd=<wallet_password>)
	cik.py reset
	cik.py status
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
W_ADDR = ""
W_PWD = ""

def init(addr, pwd, config):
	"Set addr and pwd as wallet address and wallet secret"
	config.set("user_info", "wallet.address", addr)
	config.set("user_info", "wallet.password", pwd)
	with  open("conf.cfg",'w') as cfgfile:
		config.write(cfgfile)
		print "Update successful"
	return

def printStatus():
	"Get wallet address and baalance"
	if not W_ADDR or not W_PWD:
		print "Address/Password is not set, please set these values by running:"
		print"\tcik.py init --addr=<wallet_address> --pwd=<wallet_password>"
		print "\tor"
		print"\tcik.py init -"
	else:
		#TODO: query [module] to get current balance
		print "Address:\t%s"%W_ADDR

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
	#TODO: call [module] to construct, sign and send transaction message
	return
#TODO add option to generate  brand-new addr/pwd


if __name__ == '__main__':
	#TODO Read cnf file
	arguments = docopt(__doc__,help=True, version=cik_version)
	config = ConfigParser.ConfigParser()
	config.read('conf.cfg')
	W_ADDR = config.get('user_info', 'wallet.address')
	W_PWD = config.get('user_info', 'wallet.password')
	print(arguments)
	if arguments['init']:
		if arguments['--addr'] and arguments['--pwd']:
			init(arguments['--addr'], arguments['--pwd'], config)
		else:
			init(raw_input("Your wallet address:"), getpass.getpass("Your wallet password:"), config)

	elif arguments['status']:
		printStatus()
	elif arguments['reset']:
		reset()
	elif arguments['--version']:
		print "cik Version %f"%cik_version
