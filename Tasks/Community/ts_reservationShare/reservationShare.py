#!/usr/bin/python3 -u

import time
import datetime
import json
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
import argparse
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument('--dryrun', action='store', dest='dryrun', default='true', help='perform dry run')
cmdargs, unknown = parser.parse_known_args()

reservationId = os.environ['VELOCITY_PARAM_reservationId']
baseUrl = os.environ['VELOCITY_PARAM_VELOCITY_API_ROOT']
token = os.environ['VELOCITY_PARAM_VELOCITY_TOKEN']
sharedUserIds = []

# user group admins dictionary that maps one or more user group admin to each group
adminsForGroup = {}
adminsForGroup['g2'] = ['user01', 'user02']

# get reservation details
headers={}
headers['X-Auth-Token']=token
headers['content-type']='application/json'

rlResponse = requests.get(baseUrl + '/velocity/api/reservation/v18/reservation/' + reservationId, headers=headers)
assert rlResponse.status_code == 200
reservationJson = json.loads(rlResponse.text)
print("Found reservation: " + reservationJson['name'])

rlResponse = requests.get(baseUrl + '/velocity/api/user/v9/profile/' + reservationJson['creatorId'], headers=headers)
assert rlResponse.status_code == 200
userJson = json.loads(rlResponse.text)
print("Owned by user: " + userJson['name'])

for group in userJson['groups']:
  rlResponse = requests.get(baseUrl + '/velocity/api/user/v9/group/' + group['id'], headers=headers)
  assert rlResponse.status_code == 200
  groupJson = json.loads(rlResponse.text)
  print("  Member of group: " + groupJson['name'])

  if groupJson['name'] in adminsForGroup:
    for user in adminsForGroup[groupJson['name']]:
      print("    Group admin name: " + user)
      rlResponse = requests.get(baseUrl + '/velocity/api/user/v9/profiles?filter=name::' + user, headers=headers)
      assert rlResponse.status_code == 200
      adminUserJson = json.loads(rlResponse.text)

      for adminUser in adminUserJson['profiles']:
        print("    Group admin id: " + adminUser['id'])
        sharedUserIds.append(adminUser['id'])
      
print("\nPreparing to share reservation with the following userIds: " + str(sharedUserIds))
if cmdargs.dryrun == 'false' and len(sharedUserIds) > 0:
  postData = {}
  postData['sharedUserIds'] = sharedUserIds
  rlResponse = requests.put(baseUrl + '/velocity/api/reservation/v18/reservation/' + reservationId, data=json.dumps(postData), headers=headers)
  assert rlResponse.status_code == 200
  print('\n\nReservation now shared with user group admins:')
  print(json.dumps(rlResponse.json(),indent=4))

