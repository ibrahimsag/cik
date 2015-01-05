cik
===
**Des**:  
*cik* is a minimalistic command-line bitcoin wallet.  
This project is intended to be as a proof of concept and a really simple implementation to learn from.  
Some of the decisions were made to make it simple rather than safe, a third-party service is used for the broadcast of transaction.  
It is intended to be used via testnet.


**Requirments:**  
requires docopt:  
&nbsp;&nbsp;&nbsp;&nbsp;```pip install docopt```  
requires pycoin:  
&nbsp;&nbsp;&nbsp;&nbsp;```pip install pycoin```  


**USAGE:**  
&nbsp;&nbsp;&nbsp;&nbsp;cik.py send ([-]| --recv=<receiver_wallet_address> --amount=<amount_to_be_sent>)  
&nbsp;&nbsp;&nbsp;&nbsp;cik.py init ([-]| --addr=<wallet_address> --pwd=<wallet_password>)  
&nbsp;&nbsp;&nbsp;&nbsp;cik.py reset  
&nbsp;&nbsp;&nbsp;&nbsp;cik.py status  
&nbsp;&nbsp;&nbsp;&nbsp;cik.py (-h | --help)  
&nbsp;&nbsp;&nbsp;&nbsp;cik.py --version  
**Options:**  
&nbsp;&nbsp;&nbsp;&nbsp;-h --help     Show help.  
&nbsp;&nbsp;&nbsp;&nbsp;--version     Show version.  