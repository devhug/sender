import os
import sys
import time
import base64
import threading
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
sys.path.insert(0, 'privbin')
import boto3
import module
import configuration
from termcolor import *
from botocore.exceptions import ClientError
os.environ['TZ'] = 'Asia/Jakarta'

class main:
	def __init__(self):
		self.banner = '''
██╗  ██╗██╗   ██╗ ██████╗ ███████╗███████╗███╗   ██╗██████╗ ███████╗██████╗ 
██║  ██║██║   ██║██╔════╝ ██╔════╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗
███████║██║   ██║██║  ███╗███████╗█████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██╔══██║██║   ██║██║   ██║╚════██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝╚██████╔╝███████║███████╗██║ ╚████║██████╔╝███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                        
                                                       
'''
		self.module = module.Module()
		self.sets = configuration.Sets()
		self.client = boto3.client('ses', aws_access_key_id=self.sets.aws_key, aws_secret_access_key=self.sets.aws_secret, region_name=self.sets.region)
		self.sent = 0
		self.failed = 0
		self.unkown = 0
		self.logs = 'Logs/'
		try:
			os.mkdir(self.logs)
		except:
			pass

	def get_from(self):
		frommail = self.client.list_identities()['Identities']
		resp = []
		if frommail:
			for item in frommail:
				item = item.strip()
				if '@' in item:
					resp.append(item)
				else:
					resp.append('noreply-{random}@{domain}'.format(random='{randomnum_6}', domain=item))
		if resp:
			return resp
		return False

	def pre_validate(self):
		if not os.path.isdir(self.logs):
			self.logs = 'Logs_'
		if not os.path.isfile(self.sets.letter):
			cprint("Letter {letter} is not found".format(letter=self.sets.letter), on_color='on_red')
			sys.exit()
		if not os.path.isfile(self.sets.mailist):
			cprint("Mailist file {mailist} is not found".format(mailist=self.sets.mailist), on_color='on_red')
			sys.exit()
		if self.sets.attachment != False:
			attach = []
			if isinstance(self.sets.attachment, list):
				for i in self.sets.attachment:
					if os.path.isfile(i):
						attach.append(i)
			elif isinstance(self.sets.attachment, str):
				if os.path.isfile(self.sets.attachment):
					attach.append(self.sets.attachment)
			if not attach:
				self.sets.attachment = False
			else:
				self.sets.attachment = attach
		if self.sets.tread <= 0:
			self.sets.tread = 1
			self.sets.save()
		if self.sets.fromtype.lower() == 'auto':
			self.sets.frommail = self.get_from()
		if not (self.sets.subject, self.sets.letter, self.sets.fromtype):
			self.sets.save()
		content = self.module.get_content(self.sets.mailist)
		self.data = content.splitlines()
		if not self.data:
			cprint("File %s is not found" % self.sets.mailist, on_color='on_red')
			sys.exit()
		if not self.sets.duplicate:
			self.data = list(dict.fromkeys(self.data))
		return

	def checklimit(self):
		try:
			response = self.client.get_send_quota()
			return '{sent}/{sisah}'.format(sent=response['SentLast24Hours'], sisah=response['Max24HourSend'])
		except:
			return 'Unkown'

	def send(self, countsd, _to, _from, _subject, _letter, _attach = False):
		timet = time.strftime('%I:%M %p')
		try:
			if self.sets.validate_email:
				if not self.module.validate_email(_to):
					self.module.file_append('{logs}Invalid.txt'.format(logs=self.logs), '{}\r\n'.format(_to))
					self.unkown += 1
					return False

			if _attach != False:
				_ot = [_to]
				message = MIMEMultipart()
				message['Subject'] = _subject
				message['From'] = _from
				message['To'] = ', '.join(_ot)

				# body
				part = MIMEText(_letter, 'html')
				message.attach(part)
				
				#attachment
				for i in _attach:
					filename = os.path.basename(i)
					part = MIMEApplication(open(i, 'rb').read())
					part.add_header('Content-Disposition', 'attachment', filename=filename)
					message.attach(part)

				response = self.client.send_raw_email(
					Source = _from,
					Destinations = _ot,
					RawMessage = {
						'Data': message.as_string()
					}
				)
			else:
				response = self.client.send_email(
					Source = _from,
					Destination = {
						'ToAddresses': [_to]
					},
					Message = {
						'Body': {
							self.sets.lettertype: {
								'Charset'	: self.sets.charset,
								'Data'		: _letter
							}
						},
						'Subject': {
							'Charset'	: self.sets.charset,
							'Data'		: _subject
						}
					}
				)
			submsid = response['MessageId'].split('-')[0]
			cprint("{countsd}. [{timet}] {to} [SENT/{msgid}]".format(countsd=countsd, timet=timet, to=_to, msgid=submsid), 'cyan')
			self.sent += 1
		except ClientError as e:
			if self.sets.debug:
				cprint("{countsd}. [{timet}] {to} [FAILED/{eror}]".format(countsd=countsd, timet=timet, to=_to, eror=e.response['Error']['Message']), 'red')
			else:
				cprint("{countsd}. [{timet}] {to} [FAILED]".format(countsd=countsd, timet=timet, to=_to), 'red')
			self.module.file_append('{logs}Failed.txt'.format(logs=self.logs), '{}\r\n'.format(_to))
			self.failed += 1
		except:
			if self.sets.debug:
				traceback.print_exc()
			cprint("{countsd}. {to}/[FAILED/{fm}]".format(countsd=countsd, timet=timet, to=_to, fm=_from), 'red')
			self.module.file_append('{logs}Failed.txt'.format(logs=self.logs), '{}\r\n'.format(_to))
			self.failed += 1

	def run(self):
		self.module.clearterm()
		self.pre_validate()
		cprint(self.banner, 'yellow')
		cprint("PySES By pejoh.co", 'green')
		cprint("Contact: akunretasan@hotmail.com", 'green')
		cprint("\r\n")
		time.sleep(2)
		start = time.time()
		countleft = len(self.data)
		self.emails = self.module.chunks([i.strip() for i in self.data], self.sets.tread)
		try:
			countsd = 0
			countfr = 0
			countfm = 0
			countsb = 0
			for email in self.emails:
				jumlah = len(email)
				cprint("--[ Send {jumlah} Message ]--".format(jumlah=jumlah), 'yellow', attrs=['underline'])
				threads = []
				for mail in email:
					countsd += 1
					countleft -= 1
					mail = mail.strip()
					sendfrom = '{fromname} <{frommail}>'.format(fromname=self.module.textreplace(self.sets.fromname[countfr]), frommail=self.module.textreplace(self.sets.frommail[countfm]))
					countfr += 1
					countfm += 1
					if countfr == len(self.sets.fromname):
						countfr = 0
					if countfm == len(self.sets.frommail):
						countfm = 0
					b64mail = base64.b64encode(mail)
					links = self.module.textreplace(self.sets.link.replace('{email_base64}', b64mail).replace('{email}', mail))
					subject = self.module.textreplace(self.sets.subject[countsb].replace('{email}', mail).replace('{email_base64}', b64mail).replace('{subject}', ''))
					countsb += 1
					if countsb == len(self.sets.subject):
						countsb = 0
					letter = self.module.textreplace(self.module.get_content(self.sets.letter).replace('{email}', mail).replace('{email_base64}', b64mail).replace('{link}', links).replace('{subject}', subject))
					args = (countsd, mail, sendfrom, subject, letter, self.sets.attachment)
					t = threading.Thread(target=self.send, args=args)
					threads.append(t)
				if threads:
					for t in threads:
						t.start()
					for t in threads:
						t.join()
				if countleft > 0:
					cprint("--[ {left} Email Left ]--".format(left=countleft), 'yellow', attrs=['underline'])
					if self.sets.exit_while_error:
						if self.failed >= 1:
							break
					if self.sets.sleep > 0:
						time.sleep(self.sets.sleep)
		except:
			if self.sets.debug:
				traceback.print_exc()
			else:
				cprint("SENDER ERROR", 'red')
		finally:
			cprint("Done...", 'yellow')
			elapsed_time = time.time() - start
			timer = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
			cprint("Email Sent: {sent}".format(sent=self.sent), 'cyan')
			cprint("Email Failed: {failed}".format(failed=self.failed), 'red')
			cprint("Email Unkown: {unkown}".format(unkown=self.unkown), 'red')
			cprint("Account Limit: {limit}".format(limit=self.checklimit()), 'yellow')
			cprint("Total Time: {timer}".format(timer=timer), 'yellow')

if __name__ == '__main__':
	main = main()
	main.run()