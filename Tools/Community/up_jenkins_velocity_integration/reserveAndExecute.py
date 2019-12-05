#!/usr/bin/python3 -u

from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import time
import json
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
import argparse
import sys

#parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--topologyId', action='store', dest='topologyId', help='velocity topology id')
parser.add_argument('--automationPathList', nargs='+', action='store', dest='path', help='velocity automation path list')
parser.add_argument('--user', action='store', dest='user', help='Username')
parser.add_argument('--password', action='store', dest='password', help='Password')
parser.add_argument('--baseUrl', action='store', dest='baseUrl', help='velocity base Url')
parser.add_argument('--agentPoolName', action='store', dest='poolname', help='agent pool')
parser.add_argument('--agentCallBackUrl', action='store', dest='callbackUrl', help='agent call back Url')

results, unknown = parser.parse_known_args()

#Variable declaration of parsed arguments
user = results.user
password = results.password
baseUrl = results.baseUrl
topologyId = results.topologyId
poolname = results.poolname
callbackUrl = results.callbackUrl
path = results.path


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

    
tResponse = requests.get(baseUrl + '/velocity/api/auth/v2/token', auth=HTTPBasicAuth(user, password))
token_data = json.loads(tResponse.text)
token = token_data['token']

# start callback server
httpd = HTTPServer(('0.0.0.0', 0), SimpleHTTPRequestHandler)
eventType = ''
executionID = ''
callbackPort = httpd.server_port
exitFail = False

# form the reservation invocation
headers['X-Auth-Token']=token
headers['content-type']='application/json'
postData={}
postData['topologyId']=topologyId
postData['description']='Invoked from reserveAndExecute'
postData['duration']=300
postData['name']='Python reserveAndExecute'

# Start reservation in Velocity
rlResponse = requests.post(baseUrl + '/velocity/api/reservation/v13/reservation', data=json.dumps(postData), headers=headers)
assert rlResponse.status_code == 200
reservationJson = json.loads(rlResponse.text)
reservationId = reservationJson['id']

# form the execution invocation
exPostData={}
exPostData['reservationID']=reservationId
exPostData['detailLevel']='ALL_ISSUES_ALL_STEPS'
exPostData['callbackURL']=callbackUrl + str(callbackPort)
exPostData['requirements']=[]
requirements={}
requirements['name']='pool'
requirements['value']=poolname
exPostData['requirements'].append(requirements)

# Start execution in Velocity
for exePath in path:
  exPostData['testPath']=exePath
  exResponse = requests.post(baseUrl + '/ito/executions/v1/executions', data=json.dumps(exPostData), headers=headers)
  # listen for an incoming webhook that indicates execution complete
  timeout = time.time() + 60*30  # 30 minutes from now
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
