#!/usr/bin/python3 -u
# Dec 17 completion 
# Enhancements to complete
#


from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import os
import time
import json
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
import argparse
import sys


#parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--topologyName', action='store', dest='topologyName', help='velocity name')
parser.add_argument('--automationPathList', nargs='+', action='store', dest='path', help='velocity automation path list')
parser.add_argument('--user', action='store', dest='user', help='Username')
parser.add_argument('--password', action='store', dest='password', help='Password')
parser.add_argument('--baseUrl', action='store', dest='baseUrl', help='https://VelocityUrl.com')
parser.add_argument('--reportdetailLevel', action='store', dest='detailLevel', help='velocity report detailLevel')
parser.add_argument('--testcasetimeout', action='store', dest='timeout', help='time out in min for test execution')
results, unknown = parser.parse_known_args()

#Variable declaration of parsed arguments
user = results.user
password = results.password
baseUrl = results.baseUrl
topologyName = results.topologyName
detailLevel = results.detailLevel
path = results.path
timeout = results.timeout

#determine what hostname for the callback URL
stream = os.popen('hostname -f')
callbackhost = stream.read()
callbackhost = callbackhost.rstrip("\n")
callbackURL = 'http://' + callbackhost + ':'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        global eventType
        global executionID
        global exitFail

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'Callback received')
        self.wfile.write(response.getvalue())
        dbody=json.loads(body.decode('utf-8'))
        print(json.dumps(dbody,indent=4, sort_keys=True))
        eventType = dbody['eventType']
        executionID = dbody['executionID']
        if 'executionStatus' in dbody.keys():
            if dbody['executionStatus'] != "PASS":
                print('Test case failed, exiting...')
                exitFail = True


headers={}

#Validate detail level is correct
validDetailLevel = ['ALL_ISSUES_ALL_STEPS', 'ALL_ISSUES_ERROR_STEPS', 'LAST_RESPONSE', 'ERROR_ISSUES_ONLY', 'ERROR_ISSUES_WITH_STEPS', 'REPORT_ONLY']
if detailLevel in validDetailLevel:
    print("Detail level is " + detailLevel)
else:
    print("detailLevel is not recognized" + detailLevel)
    detailLevel = 'ALL_ISSUES_ALL_STEPS'
    print("detailLevel " + detailLevel + "will be used")


#Get/Validate Token for Velocity REST session
tResponse = requests.get(baseUrl + '/velocity/api/auth/v2/token', auth=HTTPBasicAuth(user, password))
token_data = json.loads(tResponse.text)
if 'errorId' in token_data:
    print("Login Credentials invalid for " + baseUrl)
    sys.exit(1)
else:
    print("Token was successfully retrieved")
token = token_data['token']

# start callback server
httpd = HTTPServer(('0.0.0.0', 0), SimpleHTTPRequestHandler)
eventType = ''
executionID = ''
callbackPort = httpd.server_port
exitFail = False

callback = callbackURL + str(callbackPort)
# form the header
headers['X-Auth-Token']=token
headers['content-type']='application/json'

# TODO: URL encode toplogy name - Velocity topology name with special characters or spaces
#Get/Validate topologyID from Topology Name
tpResponse = requests.get(baseUrl + '/velocity/api/topology/v10/topologies/?filter=name::' + topologyName, headers=headers)
tpJson = json.loads(tpResponse.text)
if tpJson['total'] == 0:
    print("Topology does not exist on " + baseUrl)
    sys.exit(1)
topologyId = tpJson['topologies'][0]['id']
print("TopologyID is " + topologyId)

# form the reservation invocation
postData={}
postData['topologyId']=topologyId
postData['description']='Invoked from reserveAndExecute'
postData['duration']=300
postData['name']='Velocity Reserve and Execute script - Reservation'

print("CallbackURL = " + callbackURL + str(callbackPort))


# Start reservation in Velocity
rlResponse = requests.post(baseUrl + '/velocity/api/reservation/v13/reservation', data=json.dumps(postData), headers=headers)
reservationJson = json.loads(rlResponse.text)
if 'errorId' in reservationJson:
    print("Reservation Failed due to " + reservationJson['errorId'])
    sys.exit(1)
reservationId = reservationJson['id']
print("Reservation ID is "  + reservationId)

# form the execution invocation
exPostData={}
exPostData['reservationID']=reservationId
exPostData['detailLevel']=detailLevel
exPostData['callbackURL']=callback
requirements={}

# Start execution in Velocity
for exePath in path:
  exPostData['testPath']=exePath
  exResponse = requests.post(baseUrl + '/ito/executions/v1/executions', data=json.dumps(exPostData), headers=headers)
  # TODO Capture execution ID to put URL in console output
  # TODO
  exResponseJson = json.loads(exResponse.text)
  exID = exResponsJson['executionID']
  if 'errorId' in exResponseJson:
      print("Warning: Execution Failed to launch due to " + exResponseJson['errorId'])
  # listen for an incoming webhook that indicates execution complete
  else:
      print("Executing test " + exePath)
  timeout = time.time() + 60*float(timeout)
  while True:
      httpd.handle_request()
      if exitFail:
          rsResponse = requests.post(baseUrl + '/velocity/api/reservation/v13/reservation/' + reservationId + '/action?type=cancel', headers=headers)
          sys.exit(1)
      if time.time() > timeout:
          print('Timed out waiting for execution to complete')
          rsResponse = requests.post(baseUrl + '/velocity/api/reservation/v13/reservation/' + reservationId + '/action?type=cancel', headers=headers)
          sys.exit(1)
      elif eventType == 'EXECUTION_COMPLETE':
          print('\nExecution complete!\n')
          break

rsResponse = requests.post(baseUrl + '/velocity/api/reservation/v13/reservation/' + reservationId + '/action?type=cancel', headers=headers)
print('Bye bye!')
