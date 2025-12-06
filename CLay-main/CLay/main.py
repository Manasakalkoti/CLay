import asyncio
import argparse
import socket
import logging
import sys
import os
from urllib import request

# When running `python main.py` from inside the `CLay` package folder,
# Python's import path doesn't include the parent directory so `import CLay` fails.
# Add the parent folder (project root) to sys.path when run as a script so
# the package imports like `from CLay.config import *` work the same as
# when running as a module (`python -m CLay.main`).
if __name__ == '__main__':
	parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	if parent not in sys.path:
		sys.path.insert(0, parent)

# importlib
from mitmproxy import http, options
from mitmproxy.tools.dump import DumpMaster

# from config import *
# from requesthandler import *
# from responsehandler import *

from CLay.config import *
from CLay.requesthandler import RequestHandler
from CLay.responsehandler import ResponseHandler
from CLay.generate import *

logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')
class Proxy:
	def __init__(self, master):
		try:
			self.master = master
			configure.get_deception_data()
			configure.get_user_preference()
		except Exception as e:
			logging.error('Error: init main %s', e)

	def request(self, flow: http.HTTPFlow) -> None:
		try:

			# importlib.reload(sys.modules['requesthandler'])
			RequestHandler(flow)
		except Exception as e:
			logging.error('Error: request %s', e)

	def response(self, flow: http.HTTPFlow) -> None:
		try:
			# importlib.reload(sys.modules['responsehandler'])
			logging.debug("%s %s%s - %s", flow.request.method, flow.request.host, flow.request.path, flow.response.status_code)
			ResponseHandler(flow)
		except Exception as e:
			logging.error('Error: response %s', e)


async def startProxy(lhost, lport, target, cert, domain):
	try:
		proxyMode = ['reverse:' + target]
		if cert is not None:
			tlsCert = [f"[{domain}]={cert}"]
			opts = options.Options(
				listen_host=lhost,
				listen_port=lport,
				mode=proxyMode,
				certs=tlsCert
			)
		else:
			opts = options.Options(
				listen_host=lhost,
				listen_port=lport,
				mode=proxyMode,
				ssl_insecure=True
			)

		master = DumpMaster(
			opts,
			with_termlog=False,
			with_dumper=False
		)

		block_addon = master.addons.get("block")
		master.addons.remove(block_addon)
		
		if checkAvailability(lhost, lport, target):
			master.addons.add(Proxy(master))
			logging.debug('[+] Proxy starting for %s:%s', lhost, lport)
			await master.run()
			return master
		else:
			exit()
	except Exception as e:
		logging.error('Error: startProxy %s', e)

def checkAvailability(lhost, lport, target):
	flag1 = False
	flag2 = False
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(2)                                      #2 Second Timeout
		result = sock.connect_ex((lhost,lport))
		sock.close()
		if result == 0:
			logging.error("[!] Port already used, exiting...")
			flag1 = False
		else:
			flag1 = True
	except Exception as e:
			logging.error('Error: checkAvailability %s', e)
			return False
	try:
		with request.urlopen(request.Request(target, method="HEAD")) as response:
			flag2 = True
	except request.URLError:
		logging.error("[!] Destination seems unreachable, exiting...")
		flag2 = False
	except Exception as e:
		logging.error('Error: checkAvailability %s', e)
		return False

	return flag1 and flag2



def main():
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument('-c', '--config', dest='config', type=str, help='run proxy based on JSON configuration file')
		parser.add_argument('-ce', '--certs', dest='certs', help='specify path to certificate file (optional)')
		parser.add_argument('-d', '--domain', dest='domain', help='TLS domain (default=*)')

		parser.add_argument('-g', '--generate', dest='generate', action='store_true', help='generate JSON file')
		args = parser.parse_args()
		if args.config and args.config != '':
			try:
				configure.set_config(args.config)
				lhost = configure.read_config().get("listen_host")
				lport = configure.read_config().get("listen_port")
				target = configure.read_config().get("url_target")
				domain = '*'
				certs = None
				if args.certs is not None:
					certs = args.certs
					if args.domain is not None:
						domain = args.domain
				asyncio.run(startProxy(lhost=lhost, lport=lport, target=target, cert=certs, domain=domain))
			except Exception as e:
				logging.error('Error: Unable to load or parse config file %s', e)
				exit()
		elif args.generate:
			generateConfig()
	except KeyboardInterrupt:
		logging.warning('[-] KeyboardInterrupt triggered')
	except Exception as e:
		logging.error('Error: main %s', e)


if __name__ == '__main__':
	main()
