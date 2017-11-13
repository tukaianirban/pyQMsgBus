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
	payload = json.dumps({"register":"02"})
	while not ws.emitText(payload):
		time.sleep(1)
	print ("Main: Registered to channel 02 on messaging server")

	try:
		count=1
		while True:
			data = "Message counter="+str(count)
			ws.emitBinary(pickle.dumps(("01",data)))
			print ("Sent packet :", data)
			count+=1
			time.sleep(1)
	except KeyboardInterrupt:
		print ("Quitting the program just like you want")
	except:
		print ("Exception caught ! Trace: "+ traceback.format_exc())
	ws.close()

if __name__=="__main__":
	main()

