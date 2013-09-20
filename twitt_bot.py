# -*- coding:utf-8 -*-
from twitter import Twitter
from twitter import OAuth
from threading import Thread
import time
import unittest
from unittest import mock

MAX_TWITT = 140
TWITT_NUM_SPACE = 5 # 트윗 번호가 자치할 길이

class TwittBot(Thread):
	'''작업 스레드를 생성하고 일정시간마다 트윗을 올리는 클래스'''
	oauth_token = '1866109896-vPQPQ' # test values..
	oauth_secret = 'V38V7ALgjnj1iuMR'
	consumer_key = 'NtH2XF9rRmo'
	consumer_secret = '4DdjR4NHzd7diS'

	def __init__(self, db, interval_sec, callback=None):
		'''interval_sec 시간 마다 db문자열 배열을 하나씩 출력한다.'''
		super(TwittBot, self).__init__()
		self.db = db
		self.db_pos = 0
		self.interval_sec = interval_sec
		self.callback = callback

	def startFrom(self, db_index):
		self.db_pos += db_index
		self.start()

	def run(self):
		while True:
			self.doTwittJob()
			time.sleep(self.interval_sec)

	def doTwittJob(self):
		msg = self.readNextDB()
		self.twitt(msg)

	def readNextDB(self):
		msg = self.db[self.db_pos]
		self.db_pos = (self.db_pos + 1) % len(self.db)
		return msg

	def twitt(self, msg, allow_split=True):
		'''트윗 올리는 함수'''
		msg_list = TwittBot.splitTwitt(msg)
		if not allow_split and len(msg_list) > 1:
			print("twitt max len exceeded!! %s" % msg)
			return

		# login
		for m in msg_list:
			TwittBot.__twittAPI(m)
			if self.callback:
				self.callback(m)

	def __twittAPI(msg):
		twitt = Twitter(
	            auth=OAuth(TwittBot.oauth_token, TwittBot.oauth_secret,
	             TwittBot.consumer_key, TwittBot.consumer_secret)
	           )
		twitt.statuses.update(status=msg)

	def splitTwitt(msg):
		'''MAX_TWITT 수 이상의 트윗을 여러개로 자르고 각 트윗에 번호를 붙임'''
		if len(msg) <= MAX_TWITT:
			return [msg,]

		# 트윗 쪼개기
		len_each_twitt = MAX_TWITT - TWITT_NUM_SPACE
		splited = []
		temp = msg[:]
		while len(temp) > 0:
			div = min(len_each_twitt, len(temp))
			splited += [temp[0:div],]
			temp = temp[div:]

		if len(splited) < 2:
			return splited

		# 각 트윗 번호 붙이기
		for n in range(len(splited)):
			numbering = "(%d/%d)" % (n+1, len(splited))
			splited[n] = numbering + splited[n]

		return splited

# test ###############################

class TestTwittBot(unittest.TestCase):
	def setUp(self):
		# twitterAPI로 보낸 메세지 리스트
		self.twitted_msgs = []

	def onTwittMsg(self, msg):
		'''트윗 전송시 떨어지는 콜백'''
		self.twitted_msgs += [msg,]

	def testTwitt(self):
		TwittBot._TwittBot__twittAPI = mock.MagicMock()
		twittBot = TwittBot(None, 0, callback=self.onTwittMsg)
		twittBot.twitt("test")

		self.assertEqual(self.twitted_msgs, ["test",])

	def testTwittBotRun(self):
		db = ['test1','test2']
		twittBot = TwittBot(db, 1, callback=None)
		twittBot.start()

	def testSplitTwitt(self):
		long_msg = '12345678901234567890123456789012345678901234567890\
123456789012345678901234567890123456789012345678901234567890123456789012\
345678901234567890end'''
		expected = ['(1/2)12345678901234567890123456789012345678901234567890\
123456789012345678901234567890123456789012345678901234567890123456789012\
3456789012345','(2/2)67890end']
		self.assertEqual(len(expected[0]), 140)
		
		splited = TwittBot.splitTwitt(long_msg)
		self.assertEqual(splited, expected)

	def testLongTwitt(self):
		'''장문은 여러개로 쪼개져 보내져야 한다.'''
		long_msg = '12345678901234567890123456789012345678901234567890\
123456789012345678901234567890123456789012345678901234567890123456789012\
345678901234567890end'''
		expected = ['(1/2)12345678901234567890123456789012345678901234567890\
123456789012345678901234567890123456789012345678901234567890123456789012\
3456789012345','(2/2)67890end']

		TwittBot._TwittBot__twittAPI = mock.MagicMock()
		twittBot = TwittBot(None, 0, callback=self.onTwittMsg)
		twittBot.twitt(long_msg)

		self.assertEqual(self.twitted_msgs, expected)

if __name__ == "__main__":
	unittest.main()
