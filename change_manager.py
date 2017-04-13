
#
# build up a list of items that have changed state during a run
# allow the services to subscribe to changes in packages or artifacts
# restart as needed
#

class stateChangeManager:

	# dictionary of config types that have changed state on a particular server
	changedState = {}
	
	# dictionary of services that are listening for certain configuration changes
	subscribers = {}

	def __init__(self):
		print '=' * 76
		print "initializing state change manager"

	def registerStateChange(self, type, name, server):
		if name not in self.changedState:
			self.changedState[name] = { "type" :    type, \
						    "servers" : [server] }
		else:
			self.changedState[name]["servers"].append(server)

	def registerSubscriber(self, serviceName, attributes, servers):
		if serviceName not in self.subscribers:
			self.subscribers[serviceName] = { "watching" : attributes["subscribe"]["name"], \
							  "type" :     attributes["subscribe"]["type"], \
							  "servers" :  servers }			
