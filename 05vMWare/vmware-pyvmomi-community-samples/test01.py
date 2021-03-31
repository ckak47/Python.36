import atexit
import requests
from pyVim import connect
import pyvmomi

# Disable the checking of certification.
requests.packages.urllib3.disable_warnings()
# Initiate the connection to VMware vSphere.
service_instance = connect.SmartConnect(
    host="10.11.246.3",
    user="administrator@vsphere.local",
    pwd="AP!?&p@Si$rsP3V|U<Tx",
    port=443)
atexit.register(connect.Disconnect, service_instance)

# Get the session ID from the connection.
session_id = service_instance.content.sessionManager.currentSession.key
print("Session ID: %s" % session_id)