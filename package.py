# class for handling installing/uninstalling packages 

from execute import *

class package:
	servers = []
	name = None

	def install(self, changeMgr):
		for server in self.servers:
			print "checking if we need to install %s on %s" % (self.name, server)	
			# check if package is installed
			cmd = "ssh root@%s dpkg -s %s" % (server, self.name)
			(returnCode, output) = execute(cmd, printOutput=False)
			if returnCode == 0:
				print "%s is already installed on %s" % (self.name, server)
			else:
				changeMgr.registerStateChange("package", self.name, server)
				print "%s is not installed.  installing" % self.name
				cmd = "ssh root@%s apt-get install -y %s" % (server, self.name)
				(returnCode, output) = execute(cmd)	

	def uninstall(self, changeMgr):
		for server in self.servers:
			changeMgr.registerStateChange("package", self.name, server)
			print "uninstalling %s on %s" % (self.name, server)
			cmd = "ssh root@%s apt-get remove -y --purge %s" % (server, self.name)
			execute(cmd)

	def __init__(self, packageInfo, servers, changeMgr):
		print '=' * 76
		print "initializing package object"
		attributes = packageInfo["package"]
		self.servers = servers
		self.name = attributes["name"]
		print "attributes: ", attributes
		if attributes["action"] == "uninstall":
			self.uninstall(changeMgr)
		else:
			self.install(changeMgr)

