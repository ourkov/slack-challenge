
from subprocess import Popen, PIPE, STDOUT

# function for executing a command and getting it's exit code
# and also the command output
def execute(cmd, printOnly=False, printOutput=True):
	try:
		print "Executing: %s" % cmd
		if printOnly:
			return 0, "In print only mode.  No output.
		process = Popen(cmd.split(), stderr=STDOUT, stdout=PIPE)
		output = process.communicate()
		returnCode = process.wait()
		outputStr = ''
		# join stdout and stderr
		if output[0]: 
			outputStr += output[0]
		if output[1]:
			outputStr += output[1]
		if printOutput:
			print "Output: %s" % outputStr
			print "Return code: %d" % returnCode
		return returnCode, outputStr
	except:
		return 1, "Failed to execute: %s" % cmd
