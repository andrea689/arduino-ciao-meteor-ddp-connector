
from Queue import Queue
import logging
import json

import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules'))
from DDPClient import DDPClient

class DDPCiaoClient():

	def __init__(self, ddp_params, ciao_queue):
		#validate params - START
		missing_params = []
		required_params = ["host", "port"]
		for p in required_params:
			if not p in ddp_params:
				missing_params.append(p)

		if len(missing_params) > 0:
			raise RuntimeError("DDP configuration error, missing: %s" % ",".join(missing_params))

		#validate params - END

		#reference to Queue for exchanging data with CiaoCore
		self.ciao_queue = ciao_queue

		#local instance of DDP Client
		self.handle = DDPClient('ws://'+ddp_params["host"]+':'+str(ddp_params["port"])+'/websocket')
		self.handle.on('connected', self.on_connect)

		self.host = ddp_params["host"]
		self.port = ddp_params["port"]

		self.logger = logging.getLogger("ddp.client")

	def on_connect():
		self.logger.info ("Connected to DDP Server %s" % self.host)
		
	'''
	TODO from METEOR to SKETCH
	def on_message(self, client, userdata, msg):
		self.logger.debug("Got new message. Topic: %s Message: %s" % (str(msg.topic), str(msg.payload)))
		entry = {
			"data" : [str(msg.topic), str(msg.payload)]
		}
		self.ciao_queue.put(entry)
	'''
	def connect(self):
		try:
			self.handle.connect()
			return True
		except:
			return False

	def disconnect(self):
		self.handle.close()

	def callback_function(a, b):
		self.logger.debug("Callback Function. Param1: %s Param2: %s" % (str(a), str(b)))

	def publish(self, function, parameter):
		self.logger.debug("Call function: %s Parameter: %s" % (function, str(parameter)))
		try:
			self.handle.call(function, json.loads(parameter), None)
		except Exception, e:
			self.logger.error('Failed handle call: '+ str(e))