import urllib
import urllib2
import httplib
import base64
import json
#from urllib2 import Request, urlopen, URLError

class Http_ClientServer():
	def __init__(self, url):
		self.url = url
		self.base64string = ''
		self.username = 'test'
		self.password = 'testpassword'
		self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
		self.base64string = base64.b64encode('%s:%s' % (self.username, self.password))

	def set_user_agent(self, user_agent):
		self.user_agent = user_agent

	def set_user(self, username, password):
		self.username = username
		self.password = password
	
	def getAll(self):
		try:
			request = urllib2.Request(self.url + 'ciphertexts.json')
			self.add_header(request)
			self.response = urllib2.urlopen(request)
			self.add_header(request)
			print self.response.read()
		except urllib2.HTTPError, e:
			if e.code == 403: print "[Error] Authentication credentials were not provided or wrong." 
			elif e.code == 404: print "[Error] Page not found!"
			elif e.code == 400: print "[Error] Invalid Format"
			else: print "[Error]" "HTTP Error " + str(e.code)
		except urllib2.URLError:
			print "[Error] Network is unreachable!"

	def search(self, keystring):
		try:
			data = {}
			data['keystring'] = keystring
			data = urllib.urlencode(data)
			request = urllib2.Request(self.url + "ciphertexts/?" + data)
			self.add_header(request)
			response = urllib2.urlopen(request)
			result = response.read()
			print result
		except urllib2.HTTPError, e:
			if e.code == 403: print "[Error] Authentication credentials were not provided or wrong."
			elif e.code == 404: print "[Error] Page not found!"
			elif e.code == 400: print "[Error] Invalid Format"
			else: print "[Error]" "HTTP Error " + str(e.code)
		except urllib2.URLError:
			print "[Error] Network is unreachable!"

	def add_header(self, request):
		request.add_header("Authorization", "Basic %s" % self.base64string)
		request.add_header("User-Agent", self.user_agent)

	def update(self, id, keystring, ciphertext):
		try:
			data = {}
			data['keystring'] = keystring
			data['context'] = ciphertext
			data = urllib.urlencode(data)
			request = urllib2.Request(self.url + "ciphertexts/" + str(id) + "/", data)        
			self.add_header(request)
			request.get_method = lambda: 'PUT'
			response = urllib2.urlopen(request)
			print response.read()
		except urllib2.HTTPError, e:
			if e.code == 403: print "[Error] Authentication credentials were not provided or wrong." 
			elif e.code == 404: print "[Error] Page not found!"
			elif e.code == 400: print "[Error] Invalid Format"
			else: print "[Error]" "HTTP Error " + str(e.code)
		except urllib2.URLError:
			print "[Error] Network is unreachable!"

	def add(self, keystring, ciphertext):
		try:
			data = {}
			data['keystring'] = keystring
			data['context'] = ciphertext
			data = urllib.urlencode(data)
			request = urllib2.Request(self.url + "ciphertexts/", data)
			self.add_header(request)
			response = urllib2.urlopen(request)
			result = response.read()
			print result
		except urllib2.HTTPError, e:
			if e.code == 403: print "[Error] Authentication credentials were not provided or wrong." 
			elif e.code == 404: print "[Error] Page not found!"
			elif e.code == 400: print "[Error] Invalid Format"
			else: print "[Error]" "HTTP Error " + str(e.code)
		except urllib2.URLError:
			print "[Error] Network is unreachable!"

	def delete(self, id):
		try:
			request = urllib2.Request(self.url + "ciphertexts/" + str(id) + "/")
			self.add_header(request)
			request.get_method = lambda: 'DELETE' # or 'DELETE'
			response = urllib2.urlopen(request)
			print response.read()
		except urllib2.HTTPError, e:
			if e.code == 403: print "[Error] Authentication credentials were not provided or wrong." 
			elif e.code == 404: print "[Error] Page not found!"
			elif e.code == 400: print "[Error] Invalid Format"
			else: print "[Error]" "HTTP Error " + str(e.code)
		except urllib2.URLError:
			print "[Error] Network is unreachable!"
