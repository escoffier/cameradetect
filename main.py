import gevent


import select
#from socket import *
import socket
import sys
import signal
#from communication import send, receive
import xml.etree.ElementTree as ET
 
BUFSIZ = 4086
 
class Discover(object):
    def __init__(self, port=37020):
        self.deviceMap = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.server.bind(('192.168.21.206', port))
 
        signal.signal(signal.SIGINT, self.sighandler)
 
 
    def sighandler(self, signum, frame):
        print('Shutting down server...')
        self.server.close()
 
    def parseDevice(self, data):
        #print(data) 
        root = ET.fromstring(data)
        for child in root:
            if (child.tag == 'IPv4Address'):
                if(self.deviceMap.count(child.text) ==0):
                    self.deviceMap.append(child.text)
                    print(self.deviceMap)
                    #print(child.tag, child.text)
 
 
    def sendProbePkg(self):
        self.server.sendto('<?xml version="1.0" encoding="utf-8"?><Probe><Uuid>040CB6CF-DC5B-44BC-BF60-1BAAB6E4EC0C</Uuid><Types>inquiry</Types></Probe>'.encode(), ('239.255.255.250', 37020))


    def serve(self):
        inputs = [self.server,sys.stdin]
        self.outputs = []
 
        running = 1
        self.sendProbePkg()
        #self.server.sendto('<?xml version="1.0" encoding="utf-8"?><Probe><Uuid>040CB6CF-DC5B-44BC-BF60-1BAAB6E4EC0C</Uuid><Types>inquiry</Types></Probe>'.encode(), ('239.255.255.250', 37020))
        while running:
            try:
                inputready,outputready,exceptready = select.select(inputs, [], [], 3)
            except select.error:
                break

            if(len(inputready) == 0 ):
                print('time out ')
                self.sendProbePkg()
                continue
            for s in inputready:
                if(s == self.server):
                    msg, device = inputready[0].recvfrom(BUFSIZ)
                    print('device: ', device)
 
                    self.parseDevice(msg)
 
 
 
if __name__ == "__main__":
    Discover(37020).serve()

# def main():
#     pass

# if __name__ == '__main__':
#     main()