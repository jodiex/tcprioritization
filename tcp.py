import os
import xml.etree.ElementTree as ET
import glob
import json


class testPriority(object):
    alpha = 0.7 
    beta = 0.3
    theta = 0.0
    name = None
    prevPriority = 100000
    priority = 100000
    totalExecutions = 0
    totalFailures = 0
    totalPasses = 0

    def __init__(self, priorityDict=None):
        self.name = priorityDict['name']
        if priorityDict:
            self.prevPriority = priorityDict['prevPriority']
            self.totalExecutions = priorityDict['totalExecutions']
            self.totalFailures = priorityDict['totalFailures']
            self.totalPasses = priorityDict['totalPasses']

    #def set_name(self, name):
    #    self.name = name

class testCase(object):
        # name: "Create assignment",
        # time: 1.232,
        # timestamp: 2019-06-26t22:05:09,
        # tests: 45,
        # skipped: 0
        # errors: 0,
        # failures: 1
        def __init__(self,name,time,timestamp,tests,skipped,errors,failures):
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
    testPriorityFile = None
    #dictionary of testCase object, with testCase.name 
    testResultHash = {}
  
    def _init_(self, resultdirectory, testPriorityFile=None):
        self.resultdirectory = resultdirectory
        # check if resultdirectory is valid
        if (os.path.isdir(resultdirectory)):
            print(os.path.isdir(resultdirectory))
            print("I'm here!")
            # print(isdir(resultdirectory))
            if not os.listdir(resultdirectory):
                print ("empty")
            else:
                print ("not empty")
        else:
            print(os.path.isdir(resultdirectory))

            #read each file in the directory and get line <testsuite...>
            listFiles = glob.glob(resultdirectory + "/*.xml")
            testResultHash = dict()
            for x in listFiles:
                try:
                    tree = ET.parse(x)
                    root = tree.getroot()    
                    #parse line into variables 
                    name = "_".join((root.attrib.get("name")).split())
                    time = root.attrib.get("time")
                    hostname = root.attrib.get("hostname")
                    timestamp = root.attrib.get("timestamp")
                    tests = root.attrib.get("tests")
                    skipped = root.attrib.get("skipped")
                    errors = root.attrib.get("errors")
                    failures = root.attrib.get("failures")
                    self.timestamp = timestamp
                    self.hostname = hostname
                    tc = testCase(name,time,timestamp,tests,skipped,errors,failures)
                    #store tc in a dictionary
                    testResultHash[tc.name] = tc
                except Exception as e:
                    print ("ops! can not process a file {}".format(x))
                    print (e)
                    print(len(x))
                    # f = open(x, "r")
                    # print(f.read())
                    # f.close()

            
            for n, o in testResultHash.items():
                print ("test {} => {}".format(n, o))
            print ("total test cases {}".format(len(testResultHash)))
                #check if testPriorityFile exist and has permission to write

    #populated testResult object. 
    #test_case contains all test cases
    def get_test_result_data(self):
        #add code here
        pass
    
    def write_data_to_priority(self, testPriorityFile=None):
        if testPriorityFile is not None:
            outfile = testPriorityFile
        else:
            outfile = self.testPriorityFile


def calculatePriority(testCase, testPriority):
    alpha = 0.7
    beta = 0.3
    #check if testCase and testPriority are valid !!!
    testPriority['totalExecutions'] = testPriority['totalExecutions'] + testCase.tests
    testPriority['totalFailures'] = testPriority['totalFailures'] + testCase.failures
    if testCase.failures > 0:
        recentFail = 5000
    else:
        recentFail = 0
    #need to take error into account !!!!
    tcPasses = testCase.tests - testCase.failures
    testPriority['totalPasses'] = testPriority['totalPasses'] + tcPasses
    prevPrioritytemp = testPriority['prevPriority']
    testPriority['prevPriority'] = testCase.priority
    # if test fails on first run
    if testPriority['totalPasses'] == 0:
        recentFail = 5000
        failRatio = 0
    else:
        failRatio = testPriority['totalFailures'] / testPriority['totalPasses']
        testPriority['priority'] = alpha * failRatio + beta * prevPrioritytemp + recentFail
    # send to testPriorityFile
    return testPriority

def temp(resultdirectory):
    # check if resultdirectory is valid
    if (os.path.isdir(resultdirectory)):
        print(os.path.isdir(resultdirectory))
        print("I'm here!")
        # print(isdir(resultdirectory))
        if not os.listdir(resultdirectory):
             print ("empty")
        else:
             print ("not empty")
    else:
        print(os.path.isdir(resultdirectory))

    #read each file in the directory and get line <testsuite...>
    listFiles = glob.glob(resultdirectory + "/*.xml")
    testResultHash = dict()
    for x in listFiles:
        try:
            tree = ET.parse(x)
            root = tree.getroot()    
            #parse line into variables 
            name = "_".join((root.attrib.get("name")).split())
            time = root.attrib.get("time")
            timestamp = root.attrib.get("timestamp")
            tests = root.attrib.get("tests")
            skipped = root.attrib.get("skipped")
            errors = root.attrib.get("errors")
            failures = root.attrib.get("failures")
            tc = testCase(name,time,timestamp,tests,skipped,errors,failures)
            #store tc in a dictionary
            testResultHash[tc.name] = tc
        except Exception as e:
            print ("ops! can not process a file {}".format(x))
            print (e)
            print(len(x))
            # f = open(x, "r")
            # print(f.read())
            # f.close()

    #for n, o in testResultHash.items():
  #      print ("test {} => {}".format(n, o))
    print ("total test cases {}".format(len(testResultHash)))
        
        


if __name__ == "__main__":
    print("This is main...")
    #temp("C:/Users/jxiang/Downloads/test-result-28june-build/test-results/test")
    # temp("./test1")
    # temp("\\?\C:\Users\jxiang\Downloads\build\build\test-results\test2")
    temp("/Users/jxiang/Documents/TCP/temp")
    priority_file_name = '/Users/jxiang/Documents/TCP/testpriority.json'
    if os.path.exists(priority_file_name):
        jsonFile = open(priority_file_name, "r") # Open the JSON file for reading
        priority_dict = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close()
#        with open(priority_file_name, 'r') as f:
#            priority_dict = json.load(f)
        test1 = testPriority(priority_dict)
        test1.priority = calculatePriority(...)
    else:
        test1 = testPriority()
        test1.name = "Scenario..."

    priorityJSON = {
        "a": 0.7,
        "b": 0.3,
        "c": 0.0,
        "name": test1.name,
        "prevPriority": test1.prevPriority,
        "priority": test1.priority,
        "totalExecutions": test1.totalExecutions,
        "totalFailures": test1.totalFailures,
        "totalPasses": test1.totalPasses
    }

    jsonFile = open(priority_file_name, "w+")
    jsonFile.write(json.dumps(priorityJSON))
    jsonFile.close()

    #print(calculatePriority(tc, test1.Tests[0]))
    # for x in testResultHash.values():
    #    calculatePriority(x, test1.Tests[i])
    # temp("/Users/jxiang/Downloads/build/build/test-results/test2")
    # t1 = testResult("testfile", "outfile")
    # t1.write_data_to_priority()

