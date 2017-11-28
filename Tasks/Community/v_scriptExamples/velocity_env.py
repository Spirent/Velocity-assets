import os
import requests
import json

if os.environ.has_key('VELOCITY_PARAM_TMBL_FILE') is True:
  print("[INFO] TOPOLOGY FILE: " + os.environ['VELOCITY_PARAM_TMBL_FILE'])

if os.environ.has_key('VELOCITY_PARAM_RESERVATION_ID') is True:
  print("[INFO] RESERVATION ID: " + os.environ['VELOCITY_PARAM_RESERVATION_ID'])

print("[INFO] VELOCITY API ROOT: " + os.environ['VELOCITY_PARAM_VELOCITY_API_ROOT'])
print("[INFO] VELOCITY TOKEN: " + os.environ['VELOCITY_PARAM_VELOCITY_TOKEN'])
print("[INFO] BUILD PARAMETER: " + os.environ['VELOCITY_PARAM_build'])

print("\nGetting current user profile from Velocity...\n")

api = "/velocity/api/user/v7/profile/current"
headers = {"X-Auth-Token": os.environ['VELOCITY_PARAM_VELOCITY_TOKEN']}
endpoint = os.environ['VELOCITY_PARAM_VELOCITY_API_ROOT'] + api
r = requests.get(endpoint, data="", headers=headers)
print(json.dumps(r.json(), indent=2))
