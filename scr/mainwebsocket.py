# -*- coding: utf-8 -*-


from tornado.websocket import WebSocketHandler

from common.utils import Debug

from SyncMessage_pb2 import MessageLogin, MessageGenerateExistedClients, MessageLogout, ObjectInfo, WeaponInfo  #导入自定义的protobuf文件 这里要根据自己的项目自己生成

class SocketClientManager(object):
	#初始化
	def __init__(self):
		self.__room = {} #房间
		self.__clients = {} #玩家列表
		self.__weaponInfos = {} #玩家武器缓存
		self.__userInfo = {} # 玩家数据缓存
		self.__supplys = [] # 补给物品緩存
	
	numb = 0
	def add_client_to_room(self, name, client):
		for k, v in self.__room.items():
			if len(self.__room[k]) < 10:
				self.__room[k].append(name)
			else:
				numb += 1
				self.__room[numb] = []

		
	def add_client(self, name, client): #加入一个玩家
		try:
			self.__clients[name] = client 
			#result = yield from 
			self.send_message_to_new_client(client)  # 发送给新用户，其他用户的缓存数据
		except Exception as e:
			print('erroe :' + e)

	def add_weaponInfos(self, name, weaponInfo):   # 添加当前玩家武器信息武器
		if name not in self.__weaponInfos:
			self.__weaponInfos[name] = []

		self.__weaponInfos[name].append(weaponInfo)

	def update_userInfo(self, name, userInfo):  #添加玩家信息数据
		self.__userInfo[name] = userInfo

	def add_supplys(self, supplys): #添加补给物品
		self.__supplys.append(supplys)


	def remove_client(self, name):		#移除一个玩家
		if name in self.__clients:
			del self.__clients[name]

		if name in self.__weaponInfos:
			del self.__weaponInfos[name]

		if name in self.__userInfo:
			del self.__userInfo[name]

	def send_message_to_new_client(self, client): #发送其他玩家的緩存數據給新的客户端
		resp = MessageGenerateExistedClients()  # 初始化 已注册的protobuf
		resp.clients.extend(self.get_client_list())  # 将已登陆的玩家列表 转成protobuf 数据
		client.write_message(b'\x00\x22\x00\x00' + resp.SerializeToString(), binary = True)	#将protobuf数据序列化 传给 新登陆的玩家（前端使用数据生成其玩家的模型）
		#time.sleep(3)

		for k, v in self.__weaponInfos.items():   # 发送所有用户的武器缓存给新用户
			for w in v:
				client.write_message(w, binary = True)
		
		for k, v in self.__userInfo.items():   # 发送所有用户的属性缓存给新用户
			client.write_message(v, binary = True)
		#return True
		#__supplys								# 发送所有的补给缓存
		#client.write_message(v, binary = True)
	

	def send_message_to_all_except_one(self, excepted_name, message): #发送消息给除了自己以外的所有人
		for k, v in self.__clients.items():
			if k != excepted_name:
				v.write_message(message, binary = True)

	def send_message_to_sender(self, excepted_name, message):  # 发送消息给发送者
		for k, v in self.__clients.items():
			if k == excepted_name:
				v.write_message(message, binary = True)

	def get_client_list(self):  #获取玩家列表
		return self.__clients.keys()

class WebSocketHandle(WebSocketHandler):
	__client_manager = SocketClientManager()

	@classmethod
	def update_cahce(cls, chat):   #增加消息缓存
		cls.cache.append(chat)
		if len(cls.cache) > cls.cache_size:
			cls.cache = cls.cache[-cls.cache_size:]

	def open(self):				#websocket建立链接时候使用
		Debug.log('get a new connection')
		self.set_nodelay(True)
		self.__name = ''
		self.__ip =''


	def on_close(self):			#当用户断开链接
		rep = MessageLogout()
		rep.account = self.__name
		WebSocketHandle.__client_manager.send_message_to_all_except_one(self.__name, b'\x00\x01\x00\x00' + rep.SerializeToString())

		WebSocketHandle.__client_manager.remove_client(self.__name)
		Debug.log('removed: ' + self.__name)
		Debug.log('remain clients: ' + str(WebSocketHandle.__client_manager.get_client_list()))
		self.close()

	def on_message(self, message):	#收到消息的时候调用
		try:
			if message[1] == 0x00: # 0x00代表登陆（0x00是自己定义，可以随意修改成自己的标头）
				login = MessageLogin()  #初始化 登陆的protobuf
				login.ParseFromString(bytes(message[4:])) #去掉前四位标头  去后面的protobuf数据  并反序列序列化
				
				if login.account == '':
					return
				self.__name = login.account
				#self.__ip = self.
				print('liakidddd : ' +  str(self.ws_connection ))
				WebSocketHandle.__client_manager.add_client(self.__name, self) #将新登陆玩家 加入到 玩家列表中

				Debug.log('All Clienk ' + str(WebSocketHandle.__client_manager.get_client_list()))
				Debug.log('get login req from ' + self.__name)

		#	if message[1] == 0x03:   #武器数据
		#		weapon_data = WeaponInfo()
		#		weapon_data.ParseFromString(bytes(message[4:]))

#				if weapon_data.account == '':
#					return
#				WebSocketHandle.__client_manager.add_weaponInfos(weapon_data.account,message)

#			if message[1] == 0x04:   #玩家数据
#				user_data = ObjectInfo()
#				user_data.ParseFromString(bytes(message[4:]))
#
#				if user_data.account == '':
#					return
#				WebSocketHandle.__client_manager.update_userInfo(user_data.account,message)

			WebSocketHandle.__client_manager.send_message_to_all_except_one(self.__name, message) #将自己的登陆信息 传给除自己以外的其他人

		except Exception as e:
			traceback.print_exc()

