# -*- coding:utf-8 -*-
import unittest
import json
import sys
import os
import os.path

MERGE_FILE_NAME = 'db.json'
MAX_TWITT = 140

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

	tag_len = len(name) + len(author) + 2

	# parse body
	body = source[len(header):]
	sentences = []
	entries = body.split('-')
	for entry in entries:
		s = regularize(entry)
		if len(s) is 0:
			continue
		if len(s) > (MAX_TWITT - tag_len):
			print('eceeded length... %d %s' % (MAX_TWITT - len(s) - tag_len,s))
		sentences += [s,]
	result["sentences"] = sentences

	json_encoded = json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False)
	return json_encoded

def mergeFiles(dir, outPath):
	'''json 디비파일들을 하나로 통합한다.'''
	result = ('[') # 배열 선언
	for root, ds, fs in os.walk(dir):
		for f in fs:
			if f == MERGE_FILE_NAME:
				continue
			if os.path.splitext(f)[1].lower() == ".json":
				file_path = os.path.join(root, f)
				with open(file_path) as src:
					print(file_path)
					result += src.read()
					result += ',' #구분문자

	# 출력
	with open(outPath, 'w') as out:
		if result[-1] == ',':
			result = result[:-1]
		result += ']'
		out.write(result)

# Test ##########################################

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
		with open(src_path) as src, open(src_path+'.json', 'w') as out:
			source = src.read()
			encoded = parse(source)
			out.write(encoded)
	elif len(sys.argv) == 3:
		if sys.argv[1] == "merge":
			src_dir = sys.argv[2]
			mergeFiles(src_dir, os.path.join(src_dir, MERGE_FILE_NAME))

	else:
		print('''usage :''')
		print('''book_db_converter.py source_path''')
		print('''book_db_converter.py merge source_dir''')

