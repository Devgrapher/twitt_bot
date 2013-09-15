# -*- coding:utf-8 -*-
import unittest
import json
import sys

def regularize(str):
	str = str.strip('0123456789\t ')
	return str.strip('\t\n ')

def parse(source):
	result = dict()
	header = source.split('\n')[0]

	# parse header
	name, author, publisher = header.split(',')
	result["name"] = name.lstrip()
	result["author"] = author.lstrip()
	result["publisher"] = publisher.lstrip()

	# parse body
	body = source[len(header):]
	sentences = []
	entries = body.split('-')
	for entry in entries:
		s = regularize(entry)
		if len(s) is 0:
			continue
		sentences += [s,]
	result["sentences"] = sentences

	json_encoded = json.dumps(result, sort_keys=True, indent=4)
	return json_encoded

class TestDB(unittest.TestCase):
	def testParse(self):
		source = '''stanford 2005, steve jobs, stanford univ.
		you can't connect the dots -159
		looking forward - 200
		'''
		expected ='''{
    "author": "steve jobs", 
    "name": "stanford 2005", 
    "publisher": "stanford univ.", 
    "sentences": [
        "you can't connect the dots", 
        "looking forward"
    ]
}'''

		result = parse(source)
		self.assertEqual(result, expected)


if __name__ == "__main__":
	if len(sys.argv) == 1:
		unittest.main()
	elif len(sys.argv) == 2:
		src_path = sys.argv[1]
		src = open(src_path)
		out = open(src_path+'.json', 'w')

		source = src.read()
		encoded = parse(source)
		print(encoded)
		out.write(encoded)

		out.close()
		src.close()
	else:
		print('''usage : book_db_converter.py source_path''')

