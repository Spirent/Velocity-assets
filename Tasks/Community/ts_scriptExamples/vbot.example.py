import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--resourceId', action='store', dest='resourceId', help='resource ID')
parser.add_argument('--ipAddress', action='store', dest='ipAddress', help='IP address')
results, unknown = parser.parse_known_args()

print('The inventory ID of the selected resource is ' + results.resourceId)
print('The IP address of the selected resource is ' + results.ipAddress)

if os.environ.has_key('VELOCITY_PARAM_TMBL_FILE') is True:
  print("[INFO] TOPOLOGY FILE: " + os.environ['VELOCITY_PARAM_TMBL_FILE'])

if os.environ.has_key('VELOCITY_PARAM_RESERVATION_ID') is True:
  print("[INFO] RESERVATION ID: " + os.environ['VELOCITY_PARAM_RESERVATION_ID'])

if os.environ.has_key('VELOCITY_PARAM_REPORT_ID') is True:
  print("[INFO] REPORT_ID: " + os.environ['VELOCITY_PARAM_REPORT_ID'])

print("[INFO] VELOCITY API ROOT: " + os.environ['VELOCITY_PARAM_VELOCITY_API_ROOT'])
print("[INFO] VELOCITY TOKEN: " + os.environ['VELOCITY_PARAM_VELOCITY_TOKEN'])
print("[INFO] BUILD PARAMETER: " + os.environ['VELOCITY_PARAM_build'])

if os.environ.has_key('VELOCITY_PARAM_topologyResourceId') is True:
  print("[INFO] The selected resource has this ID in the topology: " + os.environ['VELOCITY_PARAM_topologyResourceId'])

if os.environ.has_key('VELOCITY_PARAM_resourceId') is True:
  print("[INFO] The selected resource has this ID in the inventory: " + os.environ['VELOCITY_PARAM_resourceId'])
