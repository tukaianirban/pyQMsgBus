The server and client implementations are both based out of Pyee messaging library (https://github.com/jfhbrook/pyee), and websockets on top.

The clients need to "register" in the server for a certain "skill". Registration packets to the server must be sent in Text format. All data packets must however be sent in Binary format. The client-side class WebSocketClientQ has functions to send the packets in Binary (.emitBinary())and Text (.emitText()) formats. The client will listen for messages with the skill, that it registered for. Once the packets are received from the server, the client will receive it in, into a collections.deque() object. The user program must manually pull out each item from the deque. 

Example:
client01.py implements a client program which registers to listen to skill "01", and polls the queue every 10msec to check for a received packet.

client02.py implements a client program which registers to listen to skill "02", and periodically sends packets with skill "01" to the messaging server. If client01.py is running and connected to the same server, then it will be able to receive these packets.

Sample codes :

Listen to a skill from the server (register on the server) :

payload = json.dumps({"register":"01"})
while not ws.emitText(payload):
        time.sleep(1)


Send messages to the server :

while True:
       data = "Message counter="+str(count)
       ws.emitBinary(pickle.dumps(("01",data)))



Poll the queue for packets from the server :

while True:
      if len(q)>0:
             pkt = q.popleft()
                    print ("Received packet : ", pickle.loads(pkt))
                    time.sleep(0.010)





