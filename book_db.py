# -*- coding:utf-8 -*-
import unittest
import json

class BookDB:
	def fromFile(path):
		'''디비파일 경로로부터 객체 생성'''
		book_db = BookDB()
		f = open(path, 'r')
		db = f.read()
		book_db.parse(db)
		f.close()
		return book_db

	def formatTag(self, str):
		return str.replace(" ", "_")

	def parse(self, db):
		'''json 형식의 디비파일을 파싱하여 문자배열로 변환한다.'''
		result = []
		books = json.loads(db)
		for book in books:
			try:
				name = self.formatTag(book["name"])
				author = self.formatTag(book["author"])
				for sentence in book["sentences"]:
					result += ["%s #%s #%s" % (sentence, author, name),]
			except KeyError as e:
				print("parse error %s %s %s" %(e, name, author))
				continue
		self.parsed = result


# test ##################################################

class TestDB(unittest.TestCase):
	def testParse(self):
		raw ='''
		[
		    {
		        "name": "stanford 2005",
		        "author": "steve jobs",
		        "sentences": [
		            "you can't connect the dots",
		            "looking forward"
		        ]
		    },
		    {
		        "name": "test"
		    }
		]
		'''
		bookdb = BookDB()
		bookdb.parse(raw)
		self.assertEqual(len(bookdb.parsed), 2)
		self.assertEqual(bookdb.parsed[0], '''you can't connect the dots #steve_jobs #stanford_2005''')
		self.assertEqual(bookdb.parsed[1], '''looking forward #steve_jobs #stanford_2005''')

	def testFromFile(self):
		bookdb = BookDB.fromFile("./test.json")
		self.assertEqual(len(bookdb.parsed), 2)
		self.assertEqual(bookdb.parsed[0], '''you can't connect the dots #steve_jobs #stanford_2005''')
		self.assertEqual(bookdb.parsed[1], '''looking forward #steve_jobs #stanford_2005''')

if __name__ == "__main__":
	unittest.main()