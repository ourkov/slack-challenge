## provision

Provision is a configuration management tool for copying files, installing/uninstalling packages and starting/stopping services on remote servers.

Usage:

./provision -c yourconfig.yaml -s server1 server2

Where 'yourconfig.yaml' is a yaml file consisting of a list of dictionaries describing server configurations and server1 and server2 are servers you wish to apply these configurations to.  It is assumed you have ssh access to each machine as root.

Provision supports three types of configurations in the configuration file: artifact, package and service.  See hello-world.yaml for an example.  Supported syntax:

### artifact

source: file to be copied - required

destination: directory or path on remote server (directories must end with '/') - required

mode: mode of remote file as you would pass to chmod

owner: owner of remote file as you would pass to chown

### package

name: name of the package - required

action: either install or uninstall.  defaults to install

### service

name: name of the service - required

action: start, stop, or restart.  this will be applied every run.

state: state you wish to have the service in.  either running or stopped.  defaults to running

subscribe: a dictionary of a configuration to watch.  must include name and type.  in the event that the subscribed configuration changes, the service will be restarted on all servers where the change occured.   





