#! /usr/bin/env python

"""cik.
USAGE:
	cik.py reset
	cik.py init ([-]| --addr=<wallet_address>)
	cik.py status
	cik.py (-h | --help)
	cik.py --version
Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt

if __name__ == '__main__':
	#TODO Read cnf file
    arguments = docopt(__doc__)
    print(arguments)
    if arguments['init']:
    	init(arguments['--addr'])
    elif arguments['status']:
    	printStatus()
    elif arguments['reset']:
    	reset()
