import os
import xml.etree.ElementTree as ET
import glob
import json

# need to consider how to take care of a modified test case
class testPriority(object):
    # This is a class representing the priority data of a test case result
    a = 0.7 
    b = 0.3
    c = 0.0
    name = None
    filename = None
    prevPriority = 10000
    priority = 10000
    totalExecutions = 0
    totalFailures = 0
    totalPasses = 0

    def __init__(self, priorityDict=None):
        if priorityDict:
            self.name = priorityDict['name']
            self.filename = None
            self.prevPriority = priorityDict['prevPriority']
            self.priority = priorityDict['priority']
            self.totalExecutions = priorityDict['totalExecutions']
            self.totalFailures = priorityDict['totalFailures']
            self.totalPasses = priorityDict['totalPasses']

class testCase(object):
    # This is a class representing a test case result
    def __init__(self,filename,name,hostname,time,timestamp,tests,skipped,errors,failures):
        self.filename=filename
        self.name=name
        self.hostname=hostname
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
    # This is a class representing all test case results from one test
    resultdirectory = None
    timestamp = None
    hostname = None
    # dictionary of testCase object, with testCase.name 
    testResultHash = {}
  
    def __init__(self, resultdirectory, timestamp, hostname, testResultHash):
        self.resultdirectory = resultdirectory
        self.timestamp = timestamp
        self.hostname = hostname
        self.testResultHash = testResultHash


def calculatePriority(testCase, testPriority):
    # check if testCase and testPriority are valid
    if testCase and testPriority:
        testPriority.totalExecutions = testPriority.totalExecutions + testCase.tests
        testPriority.totalFailures = testPriority.totalFailures + testCase.failures

        if testCase.failures > 0:
            recentFail = 5000
        else:
            recentFail = 0
        
        # take error into account
        tcPasses = testCase.tests - testCase.failures
        if tcPasses < 0:
            tcPasses = 0
        testPriority.totalPasses = testPriority.totalPasses + tcPasses
        prevPrioritytemp = testPriority.prevPriority
        testPriority.prevPriority = testPriority.priority
        # if test fails on first run, prevent division by zero
        if testPriority.totalPasses == 0:
            recentFail = 5000
            failRatio = 0
        else:
            failRatio = testPriority.totalFailures / testPriority.totalPasses

        priority_value = (testPriority.a * failRatio) + (testPriority.b * prevPrioritytemp) + recentFail
        if priority_value < 0.00001: # prevent priority values from getting infinitely small
            priority_value = 0
        return priority_value
    else:
        print("not valid")
        return 10000.

def isDirectoryValid(resultdirectory):
    # check if resultdirectory is valid
    if (os.path.isdir(resultdirectory)):
        if not os.listdir(resultdirectory):
            print ("Empty directory.")
            return False
        else:
            return True
    else:
        print ("Directory is invalid.")
        return False

def read_XML_data(resultdirectory):
    try:
        # get filename of each XML file
        base = os.path.basename(x)
        filename = os.path.splitext(base)[0]
            
        # parse XML data into variables
        tree = ET.parse(x)
        root = tree.getroot()     
        name = root.attrib.get("name")
        #name = "_".join((root.attrib.get("name")).split())
        time = float(root.attrib.get("time"))
        timestamp = root.attrib.get("timestamp")
        hostname = root.attrib.get("hostname")
        tests = int(root.attrib.get("tests"))
        skipped = int(root.attrib.get("skipped"))
        errors = int(root.attrib.get("errors"))
        failures = int(root.attrib.get("failures"))
        # store results in a testCase
        tc = testCase(filename,name,hostname,time,timestamp,tests,skipped,errors,failures)
        return tc
    except Exception as e:
        print ("ops! can not process a file {}".format(x))
        print (e)
        print(len(x))
        return None

def load_json_data(file_name, mode="r"):
    try:
        data = open(dataFilePath, mode) # Open the data JSON file for reading
        dataFile = json.load(data) # Read the JSON into the buffer
        data.close()
    except Exception as e:
        print ("loading json: {}".format(str(e)))
        return None        
    return dataFile    

def get_JSON_data(tc, priority_file_directory, dataFilePath):
    # find matching JSON file and get JSON data
    priority_file_name = priority_file_directory + tc.filename + '.json'
            
    if os.path.exists(priority_file_name): # check for an existing JSON file
        jsonFile = open(priority_file_name, "r") # Open the JSON file for reading
        priority_dict = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close()
        

        # store JSON data in a testPriority and update previous priority
        tpriority = testPriority(priority_dict)
        tpriority.prevPriority = tpriority.priority
        # calculate new priority value
        tpriority.priority = calculatePriority(tc, tpriority)

        dataFile = load_json_data(dataFilePath)
        if dataFile is None:
            # print("\n\n\ndataFile is None\n\n\n")
            dataFile = dict()
            # create_new_agg_tc(dataFilePath, tc.filename)
            # dataFile = load_json_data(dataFilePath)

        # try: # if aggregate data file is not empty
        #     # open and load JSON compiled data file
        #     # data = open(dataFilePath, "r") # Open the data JSON file for reading
        #     # dataFile = json.load(data) # Read the JSON into the buffer
        #     # data.close()
        #     dataFile = load_json_data(dataFilePath)
        # except: # if aggregate data file exists but is empty
        #     create_new_agg_tc(dataFilePath, tc.filename)
        #     dataFile = load_json_data(dataFilePath)

        if tc.filename not in dataFile:
            # print("can not find in file {}".format(tc.filename))
            new_agg_data = create_empty_agg_data(tc.filename)
            dataFile.update(new_agg_data)
            # print("Datafile: {}".format(dataFile))

        try: # if test case exists in aggregate data file
            # append new values to end of arrays
            dataFile[tc.filename]['timestamp'].append(tc.timestamp)
            dataFile[tc.filename]['priorityval'].append(tpriority.priority)
            if tpriority.totalPasses is not 0:
                failRatio = tpriority.totalFailures / tpriority.totalPasses
            else:
                failRatio = 0
            dataFile[tc.filename]['passfail'].append(failRatio)
                
            # write data to JSON compiled data file
            data = open(dataFilePath, "w+")
            data.write(json.dumps(dataFile))
            data.close()
        except: # if test case does not exist in aggregate data file
            print("test case does not exist in aggregate data file")
            create_new_agg_tc(dataFilePath, tc.filename)
            #todo add to data file and update - do we need this?

    else: # if new test case has no JSON file, create new testPriority with default numbers
        tpriority = testPriority()
        tpriority.name = tc.name
            
    tpriority.filename = priority_file_name
    return tpriority


def update_priority(tpriority):
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
    jsonFile = open(tpriority.filename, "w+")
    jsonFile.write(json.dumps(priorityJSON))
    jsonFile.close()
        
def create_new_agg_file(dataFilePath, listXMLFiles):
    for x in listXMLFiles:
        # get filename 
        base = os.path.basename(x)
        filename = os.path.splitext(base)[0]
        create_new_agg_tc(dataFilePath, filename)


def create_empty_agg_data(name):
    aggJSON = {
        name:
        {
            "timestamp": [], "passfail": [], "priorityval": []
        }
    }
    return aggJSON

def create_new_agg_tc(dataFilePath, name):
    aggJSON = create_empty_agg_data(name)

    try: # if file is not empty
        print("creating agg for {}".format(name))
        data = open(dataFilePath, "r")
        dataFile = json.load(data)
        data.close()
        
        dataFile.update(aggJSON)

        data = open(dataFilePath, "w+")
        data.write(json.dumps(dataFile))
        data.close()   
    except Exception as e: # if file is empty
        # print('create_new_agg_tc: '+str(e))
        data = open(dataFilePath, "w+")
        data.write(json.dumps(aggJSON))
        data.close()
       

         
        

if __name__ == "__main__":
    #temp("C:/Users/jxiang/Downloads/test-result-28june-build/test-results/test")
    #temp("/Users/jxiang/Documents/TCP/temp")
    # resultdirectory = input("Enter directory of XML test results (do not end in /): ") #"/Users/jxiang/Documents/TCP/test1"
    resultdirectory = "/Users/jxiang/Documents/TCP/test1"
    priority_file_directory = "/Users/jxiang/Documents/TCP/JSON/"
    dataFilePath = "/Users/jxiang/Documents/TCP/data.json"

    isValid = isDirectoryValid(resultdirectory)
    if isValid:
        # get list of all XML files in directory
        listXMLFiles = glob.glob(resultdirectory + "/*.xml")

        # initialize dictionary of testCases
        testResultHash = dict()

        # priority_file_directory = input("Enter directory of JSON files (must end in /): ") #'/Users/jxiang/Documents/TCP/JSON/'
        while not os.path.exists(priority_file_directory):
            print("Invalid.")
            priority_file_directory = input("Enter directory of JSON files (must end in /): ")
                
        # dataFilePath = input("Enter path to JSON compiled data file (must not end in /): ") #'/Users/jxiang/Documents/TCP/data.json'
        if not os.path.exists(dataFilePath):
            create_new_agg_file(dataFilePath, listXMLFiles)

        # read each XML file in the directory and get data from line <testsuite...>
        for x in listXMLFiles:
            tc = read_XML_data(resultdirectory)
            timestamp = 0
            hostname = "Invalid"
            if tc is not None:
                timestamp = tc.timestamp
                hostname = tc.hostname

                # add each testCase into dictionary testResultHash
                testResultHash[tc.name] = tc

                # proceed to get JSON data
                tpriority = get_JSON_data(tc, priority_file_directory, dataFilePath)
                update_priority(tpriority)

        # store all in testResult
        tresult = testResult(resultdirectory, timestamp, hostname, testResultHash)
        # export tResult in some way... to database?