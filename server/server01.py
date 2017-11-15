import tornado.websocket
import tornado.web
import tornado.ioloop

from utils.websocketeventhandler import websocketeventhandler

def main():

	handlerslist=[(r'/ws', websocketeventhandler), (r"/", websocketeventhandler)]
	host ='localhost'
	port=8081


	application = tornado.web.Application(handlerslist)
	application.listen(port, host)
	tornado.ioloop.IOLoop.instance().start()

if __name__=='__main__':
	main()

	
