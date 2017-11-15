from utils.WebSocketClientQ import WebSocketClientQ
from pyee import EventEmitter
from datetime import datetime

import threading, collections, json, time, traceback, pickle

def main():
	q = collections.deque()
	ws = WebSocketClientQ(q, "localhost", 8081, '/')
	threading.Thread(target=ws.run_forever).start()

	while not (ws.client and ws.client.sock and ws.client.sock.connected):
		print ("Main:Waiting for connection to messaging server")
		time.sleep(1)

	print ("Main: Connected to messaging server; Now register my interested channel")
	payload = json.dumps({"register":"01"})
	while not ws.emitText(payload):
		time.sleep(1)
	print ("Main: Registered to channel 01 on messaging server")

	try:
		while True:
			if len(q)>0:
				pkt = q.popleft()
				print ("Received packet : ", pickle.loads(pkt))
			time.sleep(0.010)
	except KeyboardInterrupt:
		print ("Quitting the program just like you want")
	except:
		print ("Exception caught ! Trace: "+ traceback.format_exc())
	ws.close()

if __name__=="__main__":
	main()

