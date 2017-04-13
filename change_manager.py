
# build up a list of services that we want to monitor
# allow the service to subscribe to changes in packages or artifacts
# restart as needed


class stateChangeManager:
	# dictionary of config types that have changed state on a particular server
	changedState = {}
	

	# dictionary of services that are listening for certain configuration changes
	subscribers = {}

	#subscribers = {
	#  serviceName : { watching : { name : "" , type : "", servers []} }
	#} 

	def __init__(self):
		print '=' * 76
		print "initializing state change manager"


	def registerStateChange(self, type, name, server):
		if name not in self.changedState:
			self.changedState[name] = { "type" : type, \
						    "servers" : [server] }
		else:
			self.changedState[name]["servers"].append(server)

			
