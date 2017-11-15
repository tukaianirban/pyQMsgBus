import tornado.websocket
import tornado.web
import tornado.ioloop

import sys, traceback, pickle, json

from datetime import datetime
from pyee import EventEmitter

eventhandler = EventEmitter()

class websocketeventhandler(tornado.websocket.WebSocketHandler):

	def __init__(self,app, req, **kwargs):
		tornado.websocket.WebSocketHandler.__init__(self, app, req, **kwargs)
		#print ("WebSocketEventHandler: New constructor spawned...")
		self.skillset=list()

	def open(self):
		print ("WebSocketEventHandler: New connection opened")


	def on_message(self, msg):
		#print ("WebSocketEventHandler: received message of length ="+str(len(msg)))
		if isinstance(msg, bytes):
			#print ("WebSocketEventHandler: received bytes type data")
			try:
				skill, data = pickle.loads(msg)
			except:
				print("WebSocketEventHandler: Could not parse received data")
				return
			eventhandler.emit(skill, msg)
			#print ("WebSocketEventHandler: Sent message to client=",msg,"with skill=",skill)
		elif isinstance(msg, str):
			#print ("WebSocketEventHandler: received str type data")
			try:
				di = json.loads(msg)
				if ('register' in di.keys()):
					data=di['register']
					print ("WebSocketEventHandler: registered new handler for skill=",data)
					@eventhandler.on(data)
					def evthandler(msger):
						self.write_message(msger, binary=True)
						#print ("WebSocketEventHandler: Sent message to client=",msger,"with skill=",data)
					self.skillset.append((data, evthandler))
				else:
					#print ("WebSocketEventHandler: registration data not found")
					pass
			except:
				print ("WebSocketEventHandler: Exception handling incoming data. Trace:", traceback.format_exc())
		else:
			print ("WebSocketEventHandler: Packet encoding not understood. Dropped packet")
			return


	def on_close(self):
		for sk,fn in self.skillset:
			eventhandler.remove_listener(sk, fn)
			#print ("WebSocketEventHandler: removed handler for skill=",sk)
		print ("WebSocketEventHandler: Connection closed down")

	def check_origin(self, o):
		return True

