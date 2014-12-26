#! /usr/bin/env python
"""cik.
USAGE:
	cik.py reset
	cik.py init ([-]| --addr=<wallet_address> --pwd=<wallet_password>)
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
	config.set("user_info", "wallet.address", addr)
	config.set("user_info", "wallet.password", pwd)
	with  open("conf.cfg",'w') as cfgfile:
		config.write(cfgfile)
		print "Update successful"
	return
def printStatus():
	if not W_ADDR or not W_PWD:
		print "Address/Password is not set, please set these values by running:"
		print"\tcik.py init --addr=<wallet_address> --pwd=<wallet_password>"
		print "\tor"
		print"\tcik.py init -"
	else:
		print "Address:\t%s"%W_ADDR

	return
def reset():
	config.set("user_info", "wallet.address", "")
	config.set("user_info", "wallet.password", "")
	with  open("conf.cfg",'w') as cfgfile:
		config.write(cfgfile)
		print "Reset successful"
	return



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
