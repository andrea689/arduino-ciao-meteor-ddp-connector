#!/usr/bin/python

import os, sys, signal
import json, logging
from Queue import Queue
import time

from ddpciao import DDPCiao
from ddpciaoclient import DDPCiaoClient

# function to handle SIGHUP/SIGTERM
def signal_handler(signum, frame):
	global logger
	logger.info("SIGNAL CATCHED %d" % signum)
	global shd
	shd["loop"] = False

#shared dictionary
shd = {}
shd["loop"] = True
shd["basepath"] = os.path.dirname(os.path.abspath(__file__)) + os.sep

#init log
logging.basicConfig(filename=shd["basepath"]+"ddp.log", level=logging.DEBUG)
logger = logging.getLogger("ddp")

#read configuration
# TODO: verify configuration is a valid JSON
json_conf = open(shd["basepath"]+"ddp.json.conf").read()
shd["conf"] = json.loads(json_conf)

#forking to make process standalone
try:
	pid = os.fork()
	if pid > 0:
		# Save child PID to file and exit parent process
		runfile = open("/var/run/ddp-ciao.pid", "w")
		runfile.write("%d" % pid)
		runfile.close()
		sys.exit(0)

except OSError, e:
	logger.critical("Fork failed")
	sys.exit(1)

ddp_queue = Queue()
ciao_queue = Queue()

try:
	ddpclient = DDPCiaoClient(shd["conf"]["params"], ciao_queue)
except Exception, e:
	logger.critical("Exception while creating DDPCiaoClient: %s" % e)
	sys.exit(1)

signal.signal(signal.SIGINT, signal.SIG_IGN) #ignore SIGINT(ctrl+c)
signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if ddpclient.connect():
	logger.info("Connected to %s" % shd['conf']['params']['host'])
	
	shd["requests"] = {}

	ciaoclient = DDPCiao(shd, ddp_queue, ciao_queue)
	ciaoclient.start()

	# endless loop until SIGHUP/SIGTERM
	while shd["loop"] :
		if not ddp_queue.empty():
			entry = ddp_queue.get()
			logger.debug("Entry %s" % entry)

			# if entry received from ciao is an "out" message
			if entry['type'] == "out":
				function = str(entry['data'][0])
				parameter = str(entry['data'][1])
			else:
				continue

			ddpclient.publish(function, parameter)

		# the sleep is really useful to prevent ciao to cap all CPU
		# this could be increased/decreased (keep an eye on CPU usage)
		# time.sleep is MANDATORY to make signal handlers work (they are synchronous in python)
		time.sleep(0.01)

	ddpclient.disconnect()
	logger.info("DDP connector is closing")
	sys.exit(0)

else:
	logger.critical("Unable to connect to %s" % shd["conf"]["params"]["host"])