# -*- coding:utf-8 -*-
from twitter import *
import unittest
from threading import Thread
import time

MAX_TWITT = 140

class TwittBot(Thread):
	'''작업 스레드를 생성하고 일정시간마다 트윗을 올리는 클래스'''
	oauth_token = '1866109896-vPQPQ' # test values..
	oauth_secret = 'V38V7ALgjnj1iuMR'
	consumer_key = 'NtH2XF9rRmo'
	consumer_secret = '4DdjR4NHzd7diS'

	def __init__(self, db, interval_sec, callback=None, test=False):
		'''interval_sec 시간 마다 db문자열 배열을 하나씩 출력한다.'''
		super(TwittBot, self).__init__()
		self.db = db
		self.db_pos = 0
		self.interval_sec = interval_sec
		self.callback = callback
		self.test = test

	def startFrom(self, db_index):
		self.db_pos += db_index
		self.start()

	def run(self):
		while True:
			self.doTwittJob()
			time.sleep(self.interval_sec)

	def doTwittJob(self):
		msg = self.readNextDB()
		print(msg)
		if not self.test:
			TwittBot.twitt(msg)
		if self.callback:
			self.callback(msg)

	def readNextDB(self):
		msg = self.db[self.db_pos]
		self.db_pos = (self.db_pos + 1) % len(self.db)
		return msg

	def twitt(msg):
		'''트윗 올리는 함수'''
		if len(msg) > MAX_TWITT:
			print("twitt max len exceeded!! %s" % msg)
			return

		twitt = Twitter(
	            auth=OAuth(TwittBot.oauth_token, TwittBot.oauth_secret,
	             TwittBot.consumer_key, TwittBot.consumer_secret)
	           )
		twitt.statuses.update(status=msg)


# test ###############################

class TestTwittBot(unittest.TestCase):
	def testTwitt(self):
		#twitt("test")
		pass
	def testTwittBotRun(self):
		db = ['test1','test2']
		twittBot = TwittBot(db, 1, callback=None, test=True)
		twittBot.start()

if __name__ == "__main__":
	unittest.main()
