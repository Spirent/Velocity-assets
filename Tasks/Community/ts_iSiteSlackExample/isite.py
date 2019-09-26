#!/usr/bin/python3

import requests
import time
import json
import fileinput
import urllib.parse
from requests.auth import HTTPBasicAuth
from collections import Counter

dryRun = True    # if True, JSON payload prints to stdout. if False, JSON payload sent as slack message
slackWebhook = 'https://hooks.slack.com/services/insertHookHere'
baseUrl = 'https://velocity.example.com'
apiUser = 'username'
apiPassword = 'password'

headers={}
headers['content-type']='application/json'

with fileinput.input() as f_input:
  for line in f_input:
    reportMsg = eval(line)
    print(reportMsg["reportMessage"]["reportId"] + ": " + reportMsg["reportMessage"]["result"])
    executionId = reportMsg["reportMessage"]["reportId"]

    sendSlack = True
    time.sleep(3)
    # get auth token
    tResponse = requests.get(baseUrl + '/velocity/api/auth/v2/token', auth=HTTPBasicAuth(apiUser, apiPassword))
    token_data = json.loads(tResponse.text)
    token = token_data['token']
    headers['X-Auth-Token']=token

    # get execution details
    exeResponse = requests.get(baseUrl + '/ito/executions/v1/executions/' + executionId, headers=headers)
    exe_data = json.loads(exeResponse.text)

    parentReportId = exe_data['parentReportId']
    testCategory = exe_data['testCategory']
    topologyPath = exe_data['topologyPath']
    cnt=Counter()
    fields=[]

    if exe_data['runlistGuid']:
      isRunlistLast = exe_data['isRunlistLast']
      if exe_data['isRunlistLast']:
        runlistGuid = exe_data['runlistGuid']
        postData=[runlistGuid]
        rlResponse = requests.post(baseUrl + '/ito/executions/v1/runlists/summary', data=json.dumps(postData), headers=headers)
        rl_data = json.loads(rlResponse.text)
        cnt['PASS'] = 0
        cnt['FAIL'] = 0
        for i in range(0,len(rl_data[0]['executions'])):
          cnt[rl_data[0]['executions'][i]['result']] += 1

        if cnt['PASS'] > 0 and cnt['FAIL'] == 0:
          result = 'Pass'
        elif cnt['FAIL'] > 0:
          result = 'Fail'
        else:
          result = 'Indeterminate'

        reportUrl = baseUrl + '/velocity/reports/runlists/' + runlistGuid + '/runlistItems'
        rldResponse = requests.get(baseUrl + '/ito/reporting/v1/runlists/' + runlistGuid, headers=headers)
        rld_data = json.loads(rldResponse.text)
        reRunUrl=baseUrl + '/velocity/library/play/runlists/' + urllib.parse.quote(rld_data['fullPath'],safe='') + '/schedule'
        testName = rld_data['name']
        userId = rld_data['user']
        fields.append({"title":"Runlist Name","value":testName,"short":False})
        runDescription = "Automated Runlist"
      else:
        sendSlack = False
    elif not exe_data['parentReportId']:
      result = exe_data['result'].lower().capitalize()
      testName = exe_data['testPath']
      userId = exe_data['userID']
      reportUrl = baseUrl + '/velocity/reports/executions/' + executionId + '/info'
      reRunUrl=baseUrl + '/velocity/library/run/automation-assets/' + urllib.parse.quote(testName,safe='') + '/schedule?rerun=true'
      reportID = exe_data['reportID']
      parentRptResponse = requests.get(baseUrl + '/ito/reporting/v1/reports?filter=parentReport::' + reportID + '&limit=200', headers=headers)
      pr_data = json.loads(parentRptResponse.text)
      if pr_data['total'] > 0:
        fields.append({"title":"Test Suite Name","value":testName,"short":False})
        runDescription = "Automated test suite"
        cnt['PASS'] = 0
        cnt['FAIL'] = 0
        for i in range(0,len(pr_data['content'])):
          cnt[pr_data['content'][i]['result']] += 1
      else:
        fields.append({"title":"Test Case Name","value":testName,"short":False})
        runDescription = "Automated test case"
    else:
      sendSlack = False

    if sendSlack:
      fields.append({"title":"Verdict","value":result,"short":True})
      fields.append({"title":"Run By","value":userId,"short":True})
      for i in cnt.items():
        fields.append({"title":i[0].lower().capitalize() + " Count","value":i[1],"short":True})

      actions=[]
      actions.append({"type":"button","text":"View Report","url":reportUrl})
      actions.append({"type":"button","text":"Run Again","url":reRunUrl})

      nval={}
      nval["pretext"]=runDescription + " just finished"
      nval["fallback"]=reportUrl
      if result == "Fail":
        nval["color"]="danger"
      elif result == "Pass":
        nval["color"]="good"
      else:
        nval["color"]="warning"
      nval["fields"]=fields
      nval["actions"]=actions

      j={}
      j['attachments']=[nval]
      jsonPayload=json.dumps(j)

      if dryRun:
          print(jsonPayload)
      else:
          requests.post(slackWebhook, data=jsonPayload)
