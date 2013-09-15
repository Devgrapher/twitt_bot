from twitt_bot import *
from book_db import *
from datetime import datetime
import sys

twitt_num = 0
LOG_PATH = 'bot.log'
g_log_file = None

def log(msg):
	time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	outstring = "[%s] %s" % (time, msg)
	print(outstring)
	g_log_file.write(outstring + '\n')
	g_log_file.flush()

def onTwittMsg(msg):
	'''트윗 전송시 떨어지는 콜백'''
	global twitt_num
	twitt_num += 1
	log("%d, %s" % (twitt_num, msg))

def main(path, interval_sec, test_mode):

	log('initializing...')

	log('load db...')
	db = BookDB.fromFile(path)
	for a in db.parsed:
		print(a)

	log('load twitt bot...')
	bot = TwittBot(db=db.parsed, interval_sec=interval_sec, callback=onTwittMsg, test=test_mode)
	TwittBot.oauth_token = '1866109896-vPQPQiwu4TF9ohelvtC7qDdHK7L6RSay0yBQMfa'
	TwittBot.oauth_secret = 'V38V7ALgjnj1iuMRFfTKTxDTYstindaSKZ8NlZufVsI'
	TwittBot.consumer_key = 'NtH2XF9rRmowtQRGSfSz7g'
	TwittBot.consumer_secret = '4DdjR4NHzd7diS9GIWu4eAHruzVx7dnU5KZVDz6Im68'

	log('running...')
	bot.startFrom(twitt_num)

	bot.join() 
	log('terminating...')

if __name__ == "__main__":
	if len(sys.argv) == 3:
		start_index = sys.argv[2] # 시작할 db인덱스가 지정된 경우.
		twitt_num = int(start_index)
	if len(sys.argv) >= 2:
		path = sys.argv[1]
	else:
		path = 'db/db.json'

	with open(LOG_PATH, 'w') as logFile:
		g_log_file = logFile
		main(path, 60 * 60, False)
