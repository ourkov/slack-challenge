import sys
from execute import *

class service:
	name = None
	action = None
	state = None
	servers = None
	subscribedTo = None

	def __init__(self, serviceInfo, servers, changeMgr):
		print '=' * 76
		print "initializing service object."
		self.servers = servers
		attributes = serviceInfo["service"]
		print attributes
		subscribe = False
		for attribute in attributes:
			if attribute == "name":
				self.name = attributes["name"]
			elif attribute == "action":
				self.action = attributes["action"]
			elif attribute == "subscribe":
				subscribe = True # unordered dictionary
		if not self.name:
			sys.stderr.writelines("Error: service object requires name")
			sys.exit(1)		
		if self.action == "restart":
			self.restart()
		elif self.action == "start":
			self.start()
		elif self.action == "stop":
			self.stop()
		if self.state == "running":
			self.verifyRunning()
		elif self.state == "stopped":
			self.verifyStopped()
		if subscribe:
			if self.name not in changeMgr.subscribers:
				changeMgr.subscribers[self.name] = { "watching" : attributes["subscribe"]["name"], \
								     "type" :     attributes["subscribe"]["type"], \
								     "servers" :  servers }

	def restart(self):
		print "restarting %s service..." % self.name
		for server in self.servers:
			cmd = "ssh root@%s service %s restart" % (server, self.name)
			execute(cmd)

        def start(self):
                print "starting %s service..." % self.name
		for server in self.servers:
                        cmd = "ssh root@%s service %s start" % (server, self.name)
                        execute(cmd)

        def stop(self):
                print "stopping %s service..." % self.name
		for server in self.servers:
                        cmd = "ssh root@%s service %s stop" % (server, self.name)
                        execute(cmd)

	def verifyRunning(self):
		for server in self.servers:
			print "verifying that %s is running on %s" % (self.name, server)
			cmd = "ssh root@%s service %s status"
			(returnCode, output) = execute(cmd)
			# status returns zero if running, non-zero if not
			if returnCode:
				print "%s is not running.  Starting."
				cmd = "ssh root@%s service %s start" % (server, self.name)
				execute(cmd)

	def verifyStopped(self):
		for server in self.servers:
			print "verifying that %s is stopped on %s" % (self.name, server)
			cmd = "ssh root@%s service %s status"
			(returnCode, output) = execute(cmd)
			# status returns zero if running, non-zero if not
			if not returnCode:
				print "%s is running.  Stopping."
				cmd = "ssh root@%s service stop"
				execute(cmd)
