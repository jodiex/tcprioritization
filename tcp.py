import os
import xml.etree.ElementTree as ET
import glob
import json


class testPriority(object):
    a = 0.7 
    b = 0.3
    c = 0.0
    name = None
    prevPriority = 10000
    priority = 10000
    totalExecutions = 0
    totalFailures = 0
    totalPasses = 0

    def __init__(self, priorityDict=None):
        if priorityDict:
            self.name = priorityDict['name']
            self.prevPriority = priorityDict['prevPriority']
            self.priority = priorityDict['priority']
            self.totalExecutions = priorityDict['totalExecutions']
            self.totalFailures = priorityDict['totalFailures']
            self.totalPasses = priorityDict['totalPasses']

    #def set_name(self, name):
    #    self.name = name

class testCase(object):

        def __init__(self,filename, name,time,timestamp,tests,skipped,errors,failures):
            self.filename=filename
            self.name=name
            self.time=time
            self.timestamp=timestamp
            self.tests=tests
            self.skipped=skipped
            self.errors=errors
            self.failures=failures
        
        def __str__(self):
            s = "time {}".format(self.time)
            s = s + " timestamp {}".format(self.timestamp)
            s = s + " tests {}".format(self.tests)
            s = s + " skipped {}".format(self.skipped)
            s = s + " errors {}".format(self.errors)
            s = s + " failures {}".format(self.failures)
            return (s)

class testResult(object):
    #This is a class representing a test result
    resultdirectory = None
    timestamp = None
    hostname = None
    #dictionary of testCase object, with testCase.name 
    testResultHash = {}
   # testPriorityFile = None
  
    def __init__(self, resultdirectory, timestamp, hostname, testResultHash):
        self.resultdirectory = resultdirectory
        self.timestamp = timestamp
        self.hostname = hostname
        self.testResultHash = testResultHash

    #populated testResult object. 
    #test_case contains all test cases
    def get_test_result_data(self):
        #add code here
        pass
    
   # def write_data_to_priority(self, testPriorityFile=None):
   #     if testPriorityFile is not None:
   #         outfile = testPriorityFile
   #     else:
   #         outfile = self.testPriorityFile


def calculatePriority(testCase, testPriority):
    #check if testCase and testPriority are valid !!!
    if testCase and testPriority:
        testPriority.totalExecutions = testPriority.totalExecutions + testCase.tests
        testPriority.totalFailures = testPriority.totalFailures + testCase.failures

        if testCase.failures > 0:
            recentFail = 5000
        else:
            recentFail = 0
        #need to take error into account !!!!
        tcPasses = testCase.tests - testCase.failures
        testPriority.totalPasses = testPriority.totalPasses + tcPasses
        prevPrioritytemp = testPriority.prevPriority
        testPriority.prevPriority = testPriority.priority
        # if test fails on first run
        if testPriority.totalPasses == 0:
            recentFail = 5000
            failRatio = 0
        else:
            failRatio = testPriority.totalFailures / testPriority.totalPasses

        # priority_value = (testPriority.a * failRatio) + (testPriority.b * prevPrioritytemp) + recentFail
        return ((testPriority.a * failRatio) + (testPriority.b * prevPrioritytemp) + recentFail)
    else:
        print("not valid")
        return 10000

def temp(resultdirectory):
    # check if resultdirectory is valid
    if (os.path.isdir(resultdirectory)):
        print("I'm here!")
        if not os.listdir(resultdirectory):
             print ("empty")
        else:
             print ("not empty")
    else:
        print(os.path.isdir(resultdirectory))

    #read each XML file in the directory and get line <testsuite...>
    listXMLFiles = glob.glob(resultdirectory + "/*.xml")
    #listJSONFiles = glob.glob(resultdirectory + "/JSON/*.json")
    testResultHash = dict()
    for x in listXMLFiles:
        try:
            base = os.path.basename(x)
            filename = os.path.splitext(base)[0]
            tree = ET.parse(x)
            root = tree.getroot()    
            #parse line into variables 
            name = root.attrib.get("name")
            #name = "_".join((root.attrib.get("name")).split())
            time = float(root.attrib.get("time"))
            timestamp = root.attrib.get("timestamp")
            hostname = root.attrib.get("hostname")
            tests = int(root.attrib.get("tests"))
            skipped = int(root.attrib.get("skipped"))
            errors = int(root.attrib.get("errors"))
            failures = int(root.attrib.get("failures"))
            #store results in a testCase
            tc = testCase(filename,name,time,timestamp,tests,skipped,errors,failures)
            # add testCase in a dictionary testResultHash
            testResultHash[tc.name] = tc
            # get JSON data
            priority_file_directory = '/Users/jxiang/Documents/TCP/JSON/'
            priority_file_name = priority_file_directory + tc.filename + '.json'
            if os.path.exists(priority_file_name):
                jsonFile = open(priority_file_name, "r") # Open the JSON file for reading
                priority_dict = json.load(jsonFile) # Read the JSON into the buffer
                jsonFile.close()

                # store in a testPriority
                tpriority = testPriority(priority_dict)
                tpriority.priority = calculatePriority(tc, tpriority)
                print(tpriority.priority)
            else: # if new test case has no JSON file
                tpriority = testPriority()
                tpriority.name = tc.name

            priorityJSON = {
                "a": tpriority.a,
                "b": tpriority.b,
                "c": tpriority.c,
                "name": tpriority.name,
                "prevPriority": tpriority.prevPriority,
                "priority": tpriority.priority,
                "totalExecutions": tpriority.totalExecutions,
                "totalFailures": tpriority.totalFailures,
                "totalPasses": tpriority.totalPasses
            }

            # update <testcase>.json file
            jsonFile = open(priority_file_name, "w+")
            jsonFile.write(json.dumps(priorityJSON))
            jsonFile.close()
        except Exception as e:
            print ("ops! can not process a file {}".format(x))
            print (e)
            print(len(x))
            # f = open(x, "r")
            # print(f.read())
            # f.close()
    tresult = testResult(resultdirectory, tc.timestamp, hostname, testResultHash)
    # export testResult in some way

    #for n, o in testResultHash.items():
        #print ("test {} => {}".format(n, o))
    #print ("total test cases {}".format(len(testResultHash)))
        
        


if __name__ == "__main__":
    #temp("C:/Users/jxiang/Downloads/test-result-28june-build/test-results/test")
    #temp("/Users/jxiang/Documents/TCP/temp")
    temp("/Users/jxiang/Documents/TCP/temp2")
    #print(calculatePriority(tc, test1.Tests[0]))
    # for x in testResultHash.values():
    #    calculatePriority(x, test1.Tests[i])
    # temp("/Users/jxiang/Downloads/build/build/test-results/test2")
    # t1 = testResult("testfile", "outfile")
    # t1.write_data_to_priority()

