# -*- coding: utf-8 -*-

import json
import random
import asyncio
import sys
from socket import *
from datetime import datetime
from platform import platform
from traceback import print_exc
from urllib.parse import unquote_plus

from tornado.concurrent import Future as TornadoFuture
from tornado.httpserver import HTTPServer
from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.web import Application, RequestHandler
from tornado.httpclient import AsyncHTTPClient
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from handlers.user import UserHandler
from handlers.ranking import RankingHandler

from common.utils import Debug, TimeUtils, md5hash
from common.database import MySQL
from common.consts import RespBody, RespCode
from model.user import UserService 
from mainwebsocket import WebSocketHandle

FULL_CFG = json.loads(open('config.json').read())
SERVER_CFG = FULL_CFG['server']
MYSQL_CFGS = FULL_CFG['mysql']
REQUEST_CFG = FULL_CFG['request_params']


@asyncio.coroutine
def initialize_database():
	for MYSQL_CFG in MYSQL_CFGS:
		Debug.log('connecting mysql at %s:%d>%s with %d pooled connection(s)' % (MYSQL_CFG['host'], MYSQL_CFG['port'], MYSQL_CFG['name'], MYSQL_CFG['maxpoolsize']))
		yield from MySQL.initialize(
			MYSQL_CFG['host'],
			MYSQL_CFG['port'],
			MYSQL_CFG['user'],
			MYSQL_CFG['passwd'],
			MYSQL_CFG['name'],
			MYSQL_CFG['id'],
			MYSQL_CFG['charset'],
			MYSQL_CFG['maxpoolsize']
		)

asyncio.get_event_loop().run_until_complete(initialize_database())

def tocoroutine(func):
	func = asyncio.coroutine(func)
	def decorator(*args, **kwargs):
		future = TornadoFuture()
		def future_done(f):
			try:
				future.set_result(f.result())
			except Exception as e:
				future.set_exception(e)
		asyncio.async(func(*args, **kwargs)).add_done_callback(future_done)
		return future
	return decorator

class MainHandler(RequestHandler):
	def initialize(self):
		self.__phone_number = ''
		self.__user_id = ''
		self.__start_time = datetime.now()
		client_ip = ''

		#未使用Nginx代理时使用 remote_ip (使用Nginx时使用获得的用户IP不正确)  使用Nginx代理时使用headers['X-Real-IP'](未使用Nginx时使用,服务器无法连接)
		try:
			client_ip = self.request.headers['X-Real-IP']
		except:
			client_ip = self.request.remote_ip

	def __response(self,resp):
		length = len(resp)

		if length > 128:
			Debug.log('response printing ignored due to its length: ' + str(length))
		else:
			Debug.log('responsed: ' + resp)

		time_cost = datetime.now() - self.__start_time   #计算这次服务所消耗的时间
		Debug.log('handled request in %d.%ss' % (time_cost.seconds, TimeUtils.convert_microseconds_delta_to_second(time_cost.microseconds, 3)))

		self.write(resp)
		self.finish()

	def __resp_okay(self, result):
		resp = RespBody.OKAY % str(json.dumps(result, separators = (',',':')))
		self.__response(resp)

	def __resp_error(self, error_code):
		resp = RespBody.ERROR % error_code
		self.__response(resp)


	@asyncio.coroutine
	def __dispath(self,req_module,req_service,req_params):
		# 将用户数据绑定至参数
		req_params['user_id'] = self.__user_id
		req_params['phone_number'] = self.__phone_number
		#根据module生成对应handler对象
		hadle_class = eval(req_module.capitalize() + 'Handler()')	#capitalize 将首字母成为大写，其他为小写

		result = yield from getattr(hadle_class,req_service)(req_params)   #开始运行这个方法

		return result

	@asyncio.coroutine
	def __try_parse_data(self):  # 检查数据合法性
		in_form = False
		in_body = False
		
		if 'data' in self.request.arguments:
			in_form = True
			
		else:
			if self.request.body != b'':
				in_body = True

		if not in_form and not in_body:
			return RespCode.NO_INPUT_DATA

		data = None

		# 判断data是否能够被正确解析为JSON对象
		try:
			data_str = ''
			if in_body:
				print(self.request.body)
				data_str = self.request.body.decode()
			elif in_form:
				data_str = self.get_argument('data')

				
			Debug.log('get request: ' + data_str)
			data_str = unquote_plus(data_str)

			data = json.loads(data_str)
		except Exception as e:
			Debug.log_error(str(e))
			return RespCode.WRONG_DATA_PARSE

		# 判断data是否为字典格式，列表格式不被允许
		if type(data) != dict:
			return RespCode.WRONG_DATA_FORMAT

		# 检查基础module参数
		if 'module' not in data:
			return RespCode.NO_INPUT_MODULE

		# 检查基础service参数
		if 'service' not in data:
			return RespCode.NO_INPUT_SERVICE

		# 检查基础parameters参数
		if 'parameters' not in data:
			return RespCode.NO_INPUT_PARAMETERS

		# 检查基础module是否被包含
		if data['module'] not in list(REQUEST_CFG.keys()):
			return RespCode.INVALID_PARAM_MODULE

		if data['service'] not in list(REQUEST_CFG[data['module']].keys()):
			return RespCode.INVALID_PARAM_SERVICE

		needed_params = REQUEST_CFG[data['module']][data['service']]
		need_session = needed_params['need_session']
	
		if need_session:
			print(data['session'])
			phone_number, user_id = yield from UserService().get_username_by_session(data['session']) 
			
			if phone_number == None:
				return RespCode.INVALID_PARAM_SESSION
			else:
				self.__phone_number = phone_number
				self.__user_id = user_id

		other_params = needed_params['params']   #需要去判定的参数列表
		
		arg_keys = list(data['parameters'].keys())   #接收的参数
		
		for needed_key in other_params:
			if needed_key in arg_keys:
				param_type_str = str(type(data['parameters'][needed_key]))  # 只取data中自己需要的信息参数
				if param_type_str.find(other_params[needed_key]) == -1: # 再次判断当前参数列表的数据类型是否匹配
					print('数据缺失...')
					return None
			else:
				return None
		return data

	@tocoroutine
	def get(self):
		if not SERVER_CFG['enable_get']:
			self.__resp_error(RespCode.METHOD_GET_NOT_ALLOWED)

		# 允许跨域访问
		# if self.request.headers.get('Access-Control-Allow-Origin') == None:
		self.set_header('Access-Control-Allow-Origin', '*')

		try:
			# 尝试解析数据
			data = yield from self.__try_parse_data()

			# 如果data解析出来是数字，说明解析存在错误
			if type(data) == int:
				self.__resp_error(data)
			else:
				result = yield from self.__dispath(
					data['module'],
					data['service'],
					data['parameters']
				)

				if result != None:
					if type(result) != int:
						# if data['session'] != '':
						# 	extra = yield from Redis.get_extra(self.__user_id)
						# 	result['extra'] = (extra if extra != None else '')
						self.__resp_okay(result)
					else:
						self.__resp_error(result)
				else:
					self.__resp_error(RespCode.UNKNOWN_ERROR)
		except Exception as e:
			self.__resp_error(RespCode.UNKNOWN_ERROR)
			print_exc()

	@tocoroutine
	def post(self):
		# 允许跨域访问
		if self.request.headers.get('Access-Control-Allow-Origin') == None:
			self.set_header('Access-Control-Allow-Origin', '*')
		try:
			# 尝试解析数据
			data = yield from self.__try_parse_data()

			# 如果data解析出来是数字，说明解析存在错误
			if type(data) == int:
				self.__resp_error(data)
			else:
				result = yield from self.__dispath(
					data['module'],
					data['service'],
					data['parameters']
				)

				if result != None: 
					if type(result) != int:
						self.__resp_okay(result)
					else:
						self.__resp_error(result)
				else:
					self.__resp_error(RespCode.UNKNOWN_ERROR)
		except Exception as e:
			self.__resp_error(RespCode.UNKNOWN_ERROR)
			print_exc()


AsyncIOMainLoop().install()
ioloop = asyncio.get_event_loop()
AsyncHTTPClient.configure('tornado.simple_httpclient.SimpleAsyncHTTPClient')
application = Application([('/user', MainHandler), (r'/WebSocket', WebSocketHandle)] , xheaders=True)

http_server = HTTPServer(application)
http_server.bind(SERVER_CFG['port'])
http_server.start(num_processes = (platform().find('Windows') != -1 and 1 or 1))
ioloop.run_forever()

