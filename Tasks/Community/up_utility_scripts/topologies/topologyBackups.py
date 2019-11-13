#!/usr/bin/python3
""" This is used to backup topologies in case they accidentally get deleted.
You can set up a nightly cron job to archive these and restore them when needed
Developed by Mike Barfield"""

import logging
import requests
import datetime
import json
import os


# Declare variables
baseUrl = 'https://my.velocity.url.com'
apiUser = 'myUsername'
apiPassword = 'myPassword'
headers = {}
headers['content-type']='application/json'
baseLogPath = '/my/backup/path/'
currentDateTime = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
logPath = baseLogPath + currentDateTime + '/'

# logging format
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Private functions

def returnJsonValue(prop,payload):
  # return prop value from JSON object
  getValue = json.loads(payload)
  return getValue[prop]

def getTopologyIds(payload):
    # Return a list of topology IDs
    payload=json.loads(payload)
    ids = []
    print(len(payload['topologies']))
    for id in range(len(payload['topologies'])):
        ids.append(payload['topologies'][id]['id'])
    return ids

def writeToFile(filename, path, payload):
    f = open(path + filename, "w")
    try:
        f.write(payload)
        pass
    except UnicodeEncodeError:
        logging.info('Error writing file: ' + filename)
        pass
    f.close()

def createLogDirectory(path):
    # define the name of the directory to be created with dateTime
    try:
        os.mkdir(path)
    except OSError:
        logging.info('Problems creating log directory: ' + path)
    else:
        logging.info('Success log directory created: ' + path)

# Create log file directory
createLogDirectory(logPath)

# Example request to test connectivity
# r = requests.get(baseUrl + '/velocity/api/util/v1/time', auth=(apiUser, apiPassword), verify=False)
# Examples return values for requests
# print(r.status_code)
# print(r.headers['content-type'])
# print(returnJsonValue('time', r.text))

# Get token and replace with token authentication to be updated later
# r = requests.get(baseUrl + '/velocity/api/auth/v2/token', auth=(apiUser, apiPassword), verify=False)
# tokenVal=returnJsonValue('token', r.text)
# headers={'Authorization': tokenVal}

# Get topologies so we can get ids for all of them on the system
r = requests.get(baseUrl + '/velocity/api/topology/v10/topologies' + '?limit=200', auth=(apiUser, apiPassword), verify=False)
logging.info('Writing topology info to file...')
# Get topology tbml for backups need total number. If count exceeds 200 script will need updated for looping
topo=json.loads(r.text)
total=len(topo['topologies'])
for count in range(total):
    topoId=topo['topologies'][count]['id']
    name = topo['topologies'][count]['name']
    headers = {'Accept': 'application/xml, application/tbml'}
    r = requests.get(baseUrl + '/velocity/api/topology/v10/topology/' + topoId, auth=(apiUser, apiPassword), verify=False, headers=headers)
    # clean_up_topo_name, remove whitespace
    name = name.replace(' ', '')
    logging.info('writing file to log: ' + name)
    writeToFile(name + '.tbml',logPath,r.text)
logging.info('Total topolgies saved: ' + str(total))