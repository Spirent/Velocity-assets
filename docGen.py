# Spirent GitHub doc script
# Creates a README.md file for every iTest project in a directory. Projects must contain a file in documentation/readme.txt to be used
# Alex Orr
#
# Latest change: Fixed issue in markdown files were newlines were not displayed correctly
# 8/11/19


import os, codecs, re
from lxml import etree

### Create title text for a file.
#    args:  headline    | etree object containing the headline field for the file
#           description | etree object containing the headline field for the file
def makeTitleText(headline, description):
    outputString = ''
    if len(headline) > 0:
        outputString = outputString + '\n### ' + headline[0].text
    if len(description) > 0:
        outputString = outputString + '\n' + description[0].text
    return(outputString)

### Create text for all procedures in a test case
#       args:  procedures    | etree object containing procedure items
def getProcs(procedures):
    outputString = ''
    for proc in procedures:
        procName = proc.xpath('@name')[0]
        if procName != 'main':
            outputString = outputString + '\n### ' + procName
            # get arguments if they exist
            arguments = proc.xpath('arguments/item')
            if len(arguments) > 0:
                outputString = outputString + "\n<table><tr><th>Argument</th><th>Description</th></tr>"
                for argument in arguments:
                    argName = '<tr><td>' + argument.xpath('@name')[0] + '</td>'
                    if len(argument.xpath('description')) > 0:
                        argDescription = '<td>'+ argument.xpath('description')[0].text +'</tr></td>'
                        outputString = outputString + '\n' + argName + argDescription
                    else:
                        outputString = outputString + '\n' + argName + '<tr></tr>'
                outputString = outputString + '</table>\n'
    return(outputString)


def main():
    projectRoots = []
    #loop through subdirectories looking for iTest projects
    for subdir, dirs, files in os.walk('.'):
        if os.path.isfile(subdir + '/.project'):
            projectRoots.append(subdir)
            print('Project File: '+subdir)

    for projectRoot in projectRoots:
        qcLibs, testCases, responseMaps, procLibs = [],[],[],[]
        try:
            readmeFile = codecs.open(projectRoot + '/documentation/readme.txt', encoding='utf-8')
        except Exception as e:
            print("Error opening readme file for project " + projectRoot + ". Project will be ignored")
            print(e)
            continue
        readme = readmeFile.read()
        readme = re.sub(r'\r?\n','  \n',readme)
        output = '### Project Information:\n' + readme + '\n ----'
        for subdir, dirs, files in os.walk(projectRoot):
            # loop through files in project
            for file in files:
                curFile = os.sep.join([subdir, file])
                #print(curFile)
                if file.endswith('.fftc'):
                    fileRoot = etree.parse(curFile)
                    # if current file is a QC lib
                    if fileRoot.xpath('general/sessionClass/@includeTestCase'):
                        #print('QC Lib found in project:' +projectRoot+' '+file)
                        # Make title
                        headline = fileRoot.xpath('general/documentation')
                        description = fileRoot.xpath('general/notes')
                        text = '## Quickcall Library: ' + file + makeTitleText(headline=headline, description=description)
                        # get descriptions for procedures
                        procedures = fileRoot.xpath('procedures/item')
                        text = text + getProcs(procedures=procedures)
                        qcLibs.append(text)
                    # if current file is a procedure library
                    elif fileRoot.xpath('general/isProcedureLibrary'):
                        #print('proc Lib found in project:' + projectRoot + ' ' + file)
                        # get headline and description
                        headline = fileRoot.xpath('general/documentation')
                        description = fileRoot.xpath('general/notes')
                        text = '## Procedure Library: ' + file + makeTitleText(headline=headline, description=description)
                        # get descriptions for procedures
                        procedures = fileRoot.xpath('procedures/item')
                        text = text + getProcs(procedures=procedures)
                        procLibs.append(text)
                    # if current file is a regular test case
                    else:
                        #print('TC found in project:' + projectRoot + ' ' + file)
                        headline = fileRoot.xpath('//testCase/general/documentation')
                        description = fileRoot.xpath('//testCase/general/notes')
                        text = '## Test Case File: ' + file + makeTitleText(headline=headline, description=description)
                        procedures = fileRoot.xpath('procedures/item')
                        text = text + getProcs(procedures=procedures)
                        testCases.append(text)
                elif file.endswith('.ffrm'):
                    #print('RM Lib found in project:' + projectRoot + ' ' + file)
                    fileRoot = etree.parse(curFile)
                    headline = fileRoot.xpath('headline')
                    description = fileRoot.xpath('notes')
                    text = '## Response Map File: ' + file + makeTitleText(headline=headline, description=description)
                    if len(headline) > 0:
                        text = text + '\n### ' + headline[0].text
                    if len(description) > 0:
                        text = text + '\n' + description[0].text
                    responseMaps.append(text)

        if len(qcLibs) > 0:
            if len(qcLibs) == 1:
                output = output + '\n1 quickcall library in project'
            else:
                output = output + '\n' + str(len(qcLibs)) + ' quickcall libraries in project'
            for qcLib in qcLibs:
                output = output + '\n' + qcLib

        if len(procLibs) > 0:
            if len(procLibs) == 1:
                output = output + '\n1 test case in project'
            else:
                output = output + '\n' + str(len(procLibs)) + ' test cases in project'
            for procLib in procLibs:
                output = output + '\n' + procLib

        if len(testCases) > 0:
            if len(testCases) == 1:
                output = output + '\n1 test case in project'
            else:
                output = output + '\n' + str(len(testCases)) + ' test cases in project'
            for testCase in testCases:
                output = output + '\n' + testCase

        if len(responseMaps) > 0:
            if len(responseMaps) == 1:
                output = output + '\n1 response map in project'
            else:
                output = output + '\n' + str(len(responseMaps)) + ' response maps in project'
            for rm in responseMaps:
                output = output + '\n' + rm

        try:
            outputFile = codecs.open(projectRoot + '/README.md', encoding='utf-8', mode='w')
            outputFile.write(output)
        except Exception as e:
            print("Can't create README.md file for project " + projectRoot)
            print(e)




if __name__ == '__main__':
    main()

