# -*- coding: utf-8 -*-

import time
import json
import asyncio
from datetime import datetime
from hashlib import sha1
import tornado
from model.base import BaseService
from tornado import httpclient
from common.utils import Debug

#import aiohttp

class AuthService(BaseService):
	IP_WHITE_LIST = set()

	@staticmethod
	@asyncio.coroutine
	def check_sms_frequency(remote_ip, phone_number):
		a = Redis.get_cache('sms-mark-ip>' + remote_ip)
		b = Redis.get_cache('sms-mark-pn>' + phone_number)
		return a is None and b is None

	@staticmethod
	@asyncio.coroutine
	def mark_sms_status(remote_ip, phone_number):
		Redis.set_cache('sms-mark-pn>' + remote_ip, '1', expire_time = 60)
		if not remote_ip.startswith('222.217.61') and not remote_ip.startswith('172.22.14'):
			Redis.set_cache('sms-mark-ip>' + remote_ip, '1', expire_time = 10)

	@asyncio.coroutine
	def sendcode(self, phone_num):
		req_headers = {
			'content-type': 'application/x-www-form-urlencoded',
			'charset': 'utf-8',
			'AppKey': '60b2752d9db873ae99da15dc4c866f1d',
			'Nonce': 'asjkdlasdjklasjdlkjopqwjjaopjdopqwjkdpoqw',
			'CurTime': str(time.mktime(datetime.now().timetuple()))
		}

		params = 'templateid=3091142&' + 'mobile={0}'.format(phone_num)
		req_hash = sha1()
		unchecked_sum = '09cc86cedf9c' + req_headers['Nonce'] + req_headers['CurTime']
		req_hash.update(unchecked_sum.encode('utf-8'))
		req_headers['CheckSum'] = req_hash.hexdigest()
		

		client = httpclient.AsyncHTTPClient()
		client.configure(None, defaults = dict(ca_certs = 'whatever'))
		try:
			resp = yield from tornado.platform.asyncio.to_asyncio_future(
				client.fetch('http://api.netease.im/sms/sendcode.action' , method = 'POST' , headers = req_headers ,  body = params)
			)
			resp = json.loads(resp.body.decode())
			return resp['code'] == 200
		except Exception as e:
			return False


	@asyncio.coroutine
	def verifycode(self,phone_num , code):
		req_headers = {
			'content-type': 'application/x-www-form-urlencoded',
			'charset': 'utf-8',
			'AppKey': '60b2752d9db873ae99da15dc4c866f1d',
			'Nonce': 'asjkdlasdjklasjdlkjopqwjjaopjdopqwjkdpoqw',
			'CurTime': str(time.mktime(datetime.now().timetuple()))
		}
		req_hash = sha1()
		unchecked_sum = '09cc86cedf9c' + req_headers['Nonce'] + req_headers['CurTime']
		req_hash.update(unchecked_sum.encode('utf-8'))
		req_headers['CheckSum'] = req_hash.hexdigest()

		# 临时强制验证蔡靖波的手机号为正确
		if phone_num == '13818520974' and code == '1234':
			return True
		elif phone_num == '18829207378' and code == '1234':
			return True
		elif phone_num == '17601344173' and code == '1234':
			return True

		params = 'mobile={0}&code={1}'.format(phone_num,code)

		client = httpclient.AsyncHTTPClient()
		try:
			resp = yield from tornado.platform.asyncio.to_asyncio_future(
				client.fetch('http://api.netease.im/sms/verifycode.action' , method = 'POST' , headers = req_headers ,  body =params )
			)
			resp = json.loads(resp.body.decode())
			return resp['code'] == 200
		except Exception as e:
			return False
	