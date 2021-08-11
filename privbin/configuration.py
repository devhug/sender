ru = lambda text: text.decode('utf-8', 'ignore')
ur = lambda text: text.encode('utf-8', 'ignore')
conf = ru('settings.ini')

class Sets:
	def __init__(self):
		## default configuration

		# aws auth
		self.region = 'us-west-1'
		self.aws_key = 'AKXXXXXXXXXXXXXXXXXX'
		self.aws_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

		# email list
		self.mailist = 'email.txt'

		# Sender Config
		self.fromtype = 'auto'
		self.frommail = 'noreply-{randomnum_6}@dharmacowgirl.com'
		self.fromname = ['SESpy PJSender']

		# Lettering Content
		self.link = 'https://www.example.com/{email_base64}/{email}'
		self.letter = 'letter/default.html'
		self.subject = 'Send from SESpy by Pejoh.co. id #{randomnum_6}'
		self.charset = 'UTF-8'
		self.lettertype = 'Html'
		self.attachment = 'file/sample.pdf'

		# Options
		self.tread = 14
		self.sleep = 0
		self.debug = False
		self.duplicate = True
		self.exit_while_error = True

		try:
			curdata = open(conf, 'rb').read().splitlines()
		except:
			self.save()
			curdata = open(conf, 'rb').read().splitlines()
		finally:
			for name, value in [ line.split(' = ', 2) for line in curdata if '=' in line and not line.startswith('#')]:
				self.__dict__[name.strip()] = eval(value.strip())

	def save(self):
		data = ''
		for name in self.__dict__.keys():
			line = name + ' = ' + repr(self.__dict__[name]) + '\r\n'
			data += line
		open(conf, 'wb').write(ur(data))
		del data