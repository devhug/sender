#!/usr/env/python
import os
import re
import json
import random
import requests

try:
	xrange = xrange
except NameError:
	xrange = range

class Module:
    def __init__(self):
        pass

    def clearterm(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def potong(self, text, start, end):
    	if text.find(start) == -1:
    		return False
    	if text.find(end) == -1:
    		return False
    	awal = text.find(start)
    	text = text[awal + len(start):]
    	end = text.find(end)
    	if end != -1:
    		text = text[:end]
    	return text

    def validate_email(self, email):
        try:
            get = requests.get('https://pejoh.co/api/ishotm.php?email={}'.format(email))
            try:
                data = json.loads(get.content)
                return data['status']
            except:
                return False
        except:
            return False

    def file_append(self, file, text):
    	fp = open(file, 'a+')
    	fp.write(text)
    	fp.close()
    	del fp

    def put_content(self, file, text):
    	fp = open(file, 'w')
    	fp.write(text)
    	fp.close()
    	del fp

    def get_content(self, file):
    	try:
    		fp = open(file, 'r')
    		data = fp.read()
    		fp.close()
    		del fp
    	except:
    		data = ''
    	return data.strip()

    def chunks(self, l, n):
    	n = max(1, n)
    	return (l[i:i+n] for i in xrange(0, len(l), n))

    def textrandom(self, jenis, length = 10):
    	jenis = jenis.lower()
    	if jenis == 'randomnum':
    		characters = '0123456789'
    	elif jenis == 'randomtextnum':
    		characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    	elif jenis == 'randomtextup':
    		characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    	elif jenis == 'randomtextlow':
    		characters = 'abcdefghijklmnopqrstuvwxyz'
    	else:
    		characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    	result_str = ''.join(random.choice(characters) for i in range(length))
    	return result_str
    
    def textreplace(self, text):
    	match = re.findall('\{(.*?)\}', text)
    	if match:
    		for i in match:
    			val = i.strip().split('_')
    			if len(val) == 2:
    				try:
    					val[1] = int(val[1])
    				except:
    					continue
    				
    				if isinstance(val[1], int):
    					has = self.textrandom(val[0], val[1])
    					rep = '{' + i + '}'
    					text = text.replace(rep, has, 1)
    	return text