# -*- coding: utf-8 -*-
import sys
from socket import *

from SyncMessage_pb2 import MessageLogin, MessageGenerateExistedClients, MessageLogout, ObjectInfo, WeaponInfo  #导入自定义的protobuf文件 这里要根据自己的项目自己生成

class UdpServer(object):
	def __init__(self):
		self.__clients = {} #玩家列表
		print('success udp')

	def tcpserver(self):
		sock = socket(AF_INET, SOCK_DGRAM)
		sock.bind(('',10041))
		sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

		while True:
			try:
				revcData, (remoteHost, remotePort) = sock.recvfrom(1024)

				if remoteHost not in self.__clients:
					self.__clients[remoteHost] = remotePort
					print("[%s:%s]new connect" % (remoteHost, remotePort))     # 接收新客户端的ip, port  

				for k, v in self.__clients.items():
					if k != remoteHost:
						print('send message to '  + str(remoteHost) +':' + str(remotePort))
						sendDataLen = sock.sendto(revcData, (k, v))

			except Exception as e:
				if remoteHost in self.__clients:
					del self.__clients[remoteHost]
					print('error : ' + str(e) + ' : ' + str(remoteHost) +':' + str(remotePort))

		sock.close()  
	
if __name__ == "__main__":
	udpserver = UdpServer()
	udpserver.tcpserver()
