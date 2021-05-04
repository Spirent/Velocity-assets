import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--resourceId', action='store', dest='resourceId', help='resource ID')
parser.add_argument('--ipAddress', action='store', dest='ipAddress', help='IP address')
results, unknown = parser.parse_known_args()

print('The inventory ID of the selected resource is ' + results.resourceId)
print('The IP address of the selected resource is ' + results.ipAddress)

if 'VELOCITY_PARAM_TMBL_FILE' in os.environ:
  print("[INFO] TOPOLOGY FILE: " + os.environ['VELOCITY_PARAM_TMBL_FILE'])

if 'VELOCITY_PARAM_RESERVATION_ID' in os.environ:
  print("[INFO] RESERVATION ID: " + os.environ['VELOCITY_PARAM_RESERVATION_ID'])

if 'VELOCITY_PARAM_REPORT_ID' in os.environ:
  print("[INFO] REPORT_ID: " + os.environ['VELOCITY_PARAM_REPORT_ID'])

print("[INFO] VELOCITY API ROOT: " + os.environ['VELOCITY_PARAM_VELOCITY_API_ROOT'])
print("[INFO] VELOCITY TOKEN: " + os.environ['VELOCITY_PARAM_VELOCITY_TOKEN'])
print("[INFO] BUILD PARAMETER: " + os.environ['VELOCITY_PARAM_build'])

if 'VELOCITY_PARAM_topologyResourceId' in os.environ:
  print("[INFO] The selected resource has this ID in the topology: " + os.environ['VELOCITY_PARAM_topologyResourceId'])

if 'VELOCITY_PARAM_resourceId' in os.environ:
  print("[INFO] The selected resource has this ID in the inventory: " + os.environ['VELOCITY_PARAM_resourceId'])
