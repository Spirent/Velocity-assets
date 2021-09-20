#!/usr/bin/python3 -u

import time
import datetime
import json
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
import base64
import argparse
import sys
import os

reservationId = os.environ['VELOCITY_PARAM_reservationId']
jiraUser = os.environ['VELOCITY_PARAM_jiraUser']
jiraPwd = os.environ['VELOCITY_PARAM_jiraPwd']
baseUrl = os.environ['VELOCITY_PARAM_VELOCITY_API_ROOT']
token = os.environ['VELOCITY_PARAM_VELOCITY_TOKEN']

# get contents of the approved Velocity request form
headers={}
headers['X-Auth-Token']=token
headers['content-type']='application/json'
#postData={}
#postData['topologyId']=results.topologyId
#postData['description']='Invoked from ' + str(os.environ['JOB_URL'])
#postData['duration']=300
#postData['name']=results.name

rlResponse = requests.get(baseUrl + '/velocity/api/reservation/v17/reservation/' + reservationId, headers=headers)
assert rlResponse.status_code == 200
reservationJson = json.loads(rlResponse.text)

rlResponse = requests.get(baseUrl + '/velocity/api/user/v9/profile/' + reservationJson['creatorId'], headers=headers)
assert rlResponse.status_code == 200
userJson = json.loads(rlResponse.text)

postData = {'fields': {'project': {'key': 'APTDEMO'}, 'summary': '', 'description': '', 'issuetype': {'name': 'Task'}}}
postData['fields']['summary'] = reservationJson['name'] + ' PoC Request'

description = "*Requested by:* " + userJson['name'] + "\n"
description += "*Created on:* " + str(datetime.datetime.fromtimestamp(reservationJson['created']/1000)) + "\n"
description += "*Reservation link:* [Velocity Reservation|" + baseUrl + "/velocity/schedule/reservations/" + reservationId + "/topology]" + "\n\n"
description += "*" + reservationJson['request']['formName'] + "Request Form:*\n"

lastGroupName = None
for i in reservationJson['request']['fields']:
  groupName = i['groupName']
  if groupName != lastGroupName:
    # create a new panel
    if lastGroupName != None:
      # panel end
      description += "{panel}\n"

    # panel start
    description += "{panel:title="+ groupName + "}\n" 

  lastGroupName = groupName
  # create table row
  if i['type'] == 'ATTACHMENT':
    description += "|*" + i['name'] + "*|[Attachment|" + baseUrl + "/velocity/api/repository/v4/asset/" + i['value'] + "?asFile=true]|\n"
  else:
    description += "|*" + i['name'] + "*|" + i['value'] + "|\n"

# panel end
description += "{panel}\n"

postData['fields']['description'] = description

headers={}
headers['content-type']='application/json'
message = jiraUser + ":" + jiraPwd
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')
headers['Authorization']='Basic ' + base64_message
rlResponse = requests.post('https://jira.spirenteng.com/rest/api/2/issue', data=json.dumps(postData), headers=headers)
assert rlResponse.status_code == 201
jiraJson = json.loads(rlResponse.text)
jiraId = jiraJson['key']
print("jiraId: " + jiraId)

headers={}
headers['X-Auth-Token']=token
headers['content-type']='application/json'

message={}
message['html'] = True
message['forAdmins'] = True
message['subject'] = 'Jira Task Created'
message['message'] = '<a href="https://jira.spirenteng.com/browse/' + jiraId + '" target="_blank">Click here to see Jira Ticket ' + jiraId + '</a>'
rlResponse = requests.post(baseUrl + '/velocity/api/message/v7/message', data=json.dumps(message), headers=headers)
assert rlResponse.status_code == 200

