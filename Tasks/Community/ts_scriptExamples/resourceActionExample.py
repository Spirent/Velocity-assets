import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--resourceId', action='store', dest='resourceId', help='resource ID')
parser.add_argument('--ipAddress', action='store', dest='ipAddress', help='IP address')
parser.add_argument('--settings', action='store', dest='settings', help='settings')
results, unknown = parser.parse_known_args()

s=r" ____     ___  _____  ___   __ __  ____      __    ___       ____    __ ______  ____  ___   ____  ";print(s)
s=r"|    \   /  _]/ ___/ /   \ |  |  ||    \    /  ]  /  _]     /    |  /  ]      ||    |/   \ |    \ ";print(s)
s=r"|  D  ) /  [_(   \_ |     ||  |  ||  D  )  /  /  /  [_     |  o  | /  /|      | |  ||     ||  _  |";print(s)
s=r"|    / |    _]\__  ||  O  ||  |  ||    /  /  /  |    _]    |     |/  / |_|  |_| |  ||  O  ||  |  |";print(s)
s=r"|    \ |   [_ /  \ ||     ||  :  ||    \ /   \_ |   [_     |  _  /   \_  |  |   |  ||     ||  |  |";print(s)
s=r"|  .  \|     |\    ||     ||     ||  .  \\     ||     |    |  |  \     | |  |   |  ||     ||  |  |";print(s)
s=r"|__|\_||_____| \___| \___/  \__,_||__|\_| \____||_____|    |__|__|\____| |__|  |____|\___/ |__|__|";print(s)
print("")
print('Example\n')

print('This parameter is automatically passed as an argument by Velocity.')
print('\tThe inventory ID of the selected resource is ' + results.resourceId)
print('This parameter is passed because it was specified in the manifest file, but user is not prompted.')
print('\tThe IP address of the selected resource is ' + results.ipAddress)
print('This parameter is passed because it was specified in the manifest file, and user is prompted.')
print('\tThe user wants to reboot the device with these settings: ' + results.settings)
print('')

if 'VELOCITY_PARAM_TMBL_FILE' in os.environ:
  print("[INFO] TOPOLOGY FILE: " + os.environ['VELOCITY_PARAM_TMBL_FILE'])

if 'VELOCITY_PARAM_RESERVATION_ID' in os.environ:
  print("[INFO] RESERVATION ID: " + os.environ['VELOCITY_PARAM_RESERVATION_ID'])

if 'VELOCITY_PARAM_REPORT_ID' in os.environ:
  print("[INFO] REPORT_ID: " + os.environ['VELOCITY_PARAM_REPORT_ID'])

print("[INFO] VELOCITY API ROOT: " + os.environ['VELOCITY_PARAM_VELOCITY_API_ROOT'])
print("[INFO] VELOCITY TOKEN: " + os.environ['VELOCITY_PARAM_VELOCITY_TOKEN'])
print("[INFO] DEBUG PARAMETER: " + os.environ['VELOCITY_PARAM_debug_level'])

if 'VELOCITY_PARAM_topologyResourceId' in os.environ:
  print("[INFO] The selected resource has this ID in the topology: " + os.environ['VELOCITY_PARAM_topologyResourceId'])

if 'VELOCITY_PARAM_resourceId' in os.environ:
  print("[INFO] The selected resource has this ID in the inventory: " + os.environ['VELOCITY_PARAM_resourceId'])
