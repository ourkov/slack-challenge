
import hashlib
import os
import sys
from execute import *

class artifact:
	source = None
	destination = None
	mode = None
	owner = None
	servers = None

	def __init__(self, artifactInfo, servers, changeMgr):
		attributes = artifactInfo["artifact"]
		print '=' * 76
		print "initializing artifact object"
		self.servers = servers
		for attribute in attributes:
			if attribute == 'source':
				self.source = attributes['source']
			elif attribute == 'destination':
				self.destination = attributes['destination']
			elif attribute == 'mode':
				self.mode = attributes['mode']
			elif attribute == 'owner':
				self.owner = attributes['owner']
	        if not self.servers:
	            sys.stderr.writelines("Error: no servers to copy artifact to")
	            sys.exit(1)
	        if not self.source or not self.destination:
	            sys.stderr.writelines("Error: need to specify artifact source and destination")
		
	        if not os.path.isfile(self.source):
	            sys.stderr.writelines("Error: artifact source %s does not exist" % self.source)
        	# if destination is a directory, add file name
       		if not os.path.basename(self.destination):
                	self.destination = self.destination + os.path.basename(self.source)
		self.copyArtifact(changeMgr)

	def changeMode(self, server):
		print "changing mode"
		cmd = "ssh root@%s chmod %s %s" % (server, self.mode, self.destination)
		execute(cmd)

	def changeOwner(self, server):
		print "changing owner"
		cmd = "ssh root@%s chown %s %s" % (server, self.owner, self.destination)

	# check to see if we should copy file
	# if file does not exist or if sha1 has changed
	# then we should copy
	def isOutOfDate(self, server):
		print "checking if %s is out of date on %s" % (self.destination, server)
		(returnCode, output) = execute("ssh root@%s [ -f %s ]" % (server, self.destination))
		if returnCode:
			# non-zero means file does not exist
			print "%s does not exist" % self.destination
			return True
		localSha = hashlib.sha1(file(self.source, 'r').read()).hexdigest()
		(returnCode, output) = execute("ssh root@%s sha1sum %s | awk '{ print $1 }'" % (server, self.destination))
		remoteSha = output.strip()
		print "File exists.  Comparing shas"
		print "Local sha: %s" % localSha
		print "Remote sha: %s" % remoteSha
		if localSha != remoteSha:
			print "Shas do NOT match"
			return True
		else:
			print "Shas match"
			return False

	def copyArtifact(self, changeMgr):
		print "In copy artifact method"
        	for server in self.servers:
			if self.isOutOfDate(server):	            
				changeMgr.registerStateChange("artifact", self.destination, server)
				cmd = "scp %s root@%s:%s" % (self.source, server, self.destination)
	           		execute(cmd)
				if self.mode:
					self.changeMode(server)
				if self.owner:
					self.changeOwner(server)
			else:
				print "%s is up to date.  Skipping copy." % self.destination




