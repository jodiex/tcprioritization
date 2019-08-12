import os
import xml.etree.ElementTree as ET
import glob
import json
from math import pow, exp, sqrt, pi

# Todo Do we need this?
def isDirectoryValid(resultdirectory):
    # Check if resultdirectory is valid.
    if (os.path.isdir(resultdirectory)):
        if not os.listdir(resultdirectory):
            print ("Empty directory.")
            return False
        else:
            return True
    else:
        print ("Directory is invalid.")
        return False

# Todo need to consider how to take care of a modified test case.

class testPriority(object):
    # This is a class representing the priority data of a test case result.
    a = 0.7 
    b = 0.3
    c = 0.0
    failSpike = 5000
    # Guassian distribution variables.
    # See "Testing Priority" spreadsheet on google drive in the "Coop Playground" folder for more details
    gauissianMean = 0.35
    standardDeviation = 0.1
    attenuationRamp = 1
    # historyLength is the value that test cases are considered "recent" and will be taken into account for the gaussian curve
    historyLength = 100

    def __init__(self):
        name = None
        filename = None
        prevPriority = 10000
        priority = 10000
        totalExecutions = 0
        totalFailures = 0
        totalPasses = 0
        # Number of failures in the last 'historyLength' runs
        recentFailure = 0

    def _set_proirity(self, priority_dict):
        self.name = priority_dict['name']
        self.prevPriority = priority_dict['prevPriority']
        self.priority = priority_dict['priority']
        self.totalExecutions = priority_dict['totalExecutions']
        self.totalFailures = priority_dict['totalFailures']
        self.totalPasses = priority_dict['totalPasses']
        self.recentFailure = priority_dict['recentFailure']

    def process_priority(self, test_case, priority_file_directory):
        self.update_priority_from_file(test_case, priority_file_directory)
        self.calculate_priority(test_case)
        self.update_priority()

    def update_priority_from_file(self, test_case, priority_file_directory):
        # Find matching JSON file and get JSON data.
        priority_file_name = priority_file_directory + "/" + test_case.filename + ".json"

        if os.path.exists(priority_file_name): # Check for an existing JSON file.
            json_file = open(priority_file_name, "r") # Open the JSON file for reading.
            priority_dict = json.load(json_file) # Read the JSON into the buffer.
            json_file.close()
            self._set_proirity(priority_dict)
        print("test cases {}".format(test_case.name))

        self.name = test_case.name
        self.filename = priority_file_name

    def calculate_priority(self, test_case):
        # Currently tests under "skipped" and "errors" are not taken into account.
        self.totalExecutions = self.totalExecutions + 1
        if((test_case.failures > 0) or (test_case.skipped > 0) or (test_case.errors > 0)):
            self.totalFailures = self.totalFailures + 1
            spike = self.failSpike
        else:
            self.totalPasses = self.totalPasses + 1
            spike = 0

        self.prevPriority = self.priority
        print("\nprev value {}".format(self.prevPriority))
        # if test fails on first run, prevent division by zero
        if self.totalPasses == 0:
            failRatio = 0
        else:
            failRatio = self.totalFailures / self.totalPasses

        # Need to pull most recent fails from database.
        self.update_recentFailure(test_case)
        # Using functions from "import math"
        exponent = pow((self.recentFailure/self.historyLength - self.gauissianMean), 2)/(-2*pow(self.standardDeviation, 2))
        Gcurve = exp(exponent)/(4*sqrt(2*pi()*pow(self.standardDeviation, 2)))
        priority_value = (self.a * failRatio) + (self.b * self.prevPriority) + (1-Gcurve)*spike + self.prevPriority*Gcurve*(self.attenuationRamp-self.b)
        print("\nnew value {}".format(priority_value))
        if priority_value < 0.00001: # prevent priority values from getting infinitely small
            priority_value = 0
        self.priority = priority_value

    def update_recentFailure(self, test_case)
        # Need to pull the test results from position historyLength to historyLength-x where x is test_case.tests - test_case.skipped.
        # Decrement self.recentFailure for each failure in the pulled records as they will be leaving the 100 test range.
        # Then do (self.recentFailure + test_case.failures) as these failures will be entering the 100 test range.
        # Could also implement a variable history length to allow user to define how far back they want to look.
        return 0

    def update_priority(self):
        priorityJSON = {
            "a": self.a,
            "b": self.b,
            "c": self.c,
            "name": self.name,
            "prevPriority": self.prevPriority,
            "priority": self.priority,
            "totalExecutions": self.totalExecutions,
            "totalFailures": self.totalFailures,
            "totalPasses": self.totalPasses,
            "recentFailure": self.recentFailure
        }

        print ("tpriority.filename {}".format(self.filename))
        # Update <testcase>.json file
        jsonFile = open(self.filename, "w+")
        jsonFile.write(json.dumps(priorityJSON))
        jsonFile.close()

    def create_empty_agg_data(self, name):
        aggJSON = {
            name:
            {
                "timestamp": [], "passfail": [], "priorityval": []
            }
        }
        return aggJSON

    def load_json_data(self, file_name, mode="r"):
        try:
            data = open(file_name, mode) # Open the data JSON file for reading
            dataFile = json.load(data) # Read the JSON into the buffer
            data.close()
        except Exception as e:
            print ("loading json: {}".format(str(e)))
            return None
        return dataFile

    def create_new_agg_tc(self, data_file_path, name):
        agg_json = self.create_empty_agg_data(name)

        try: # if file is not empty
            print("creating agg for {}".format(name))
            data = open(data_file_path, "r")
            data_file = json.load(data)
            data.close()

            data_file.update(agg_json)

            data = open(data_file_path, "w+")
            data.write(json.dumps(data_file))
            data.close()
        except Exception as e: # if file is empty
            # print('create_new_agg_tc: '+str(e))
            data = open(data_file_path, "w+")
            data.write(json.dumps(agg_json))
            data.close()

    def update_agg(self, data_file_path, test_case):
        dataFile = self.load_json_data(data_file_path)
        if dataFile is None:
            # print("\n\n\ndataFile is None\n\n\n")
            dataFile = dict()

        if test_case.filename not in dataFile:
            # print("can not find in file {}".format(tc.filename))
            new_agg_data = self.create_empty_agg_data(test_case.filename)
            dataFile.update(new_agg_data)
            # print("Datafile: {}".format(dataFile))

        try: # if test case exists in aggregate data file
            # append new values to end of arrays
            dataFile[test_case.filename]['timestamp'].append(test_case.timestamp)
            dataFile[test_case.filename]['priorityval'].append(self.priority)
            if self.totalPasses is not 0:
                failRatio = self.totalFailures / self.totalPasses
            else:
                failRatio = 0
            dataFile[test_case.filename]['passfail'].append(failRatio)

            # write data to JSON compiled data file
            data = open(data_file_path, "w+")
            data.write(json.dumps(dataFile))
            data.close()
        except: # if test case does not exist in aggregate data file
            print("test case does not exist in aggregate data file")
            self.create_new_agg_tc(data_file_path, test_case.filename)

    def __str__(self):

        s = "testPriority\nfilename {}".format(self.filename)
        s = s+" name {}\n".format(self.name)
        s = s + " prevPriority {}".format(self.prevPriority)
        s = s + " priority {}".format(self.priority)
        s = s + " totalExecutions {}".format(self.totalExecutions)
        s = s + " totalFailures {}".format(self.totalFailures)
        s = s + " totalPasses {}".format(self.totalPasses)
        s = s + " a: {}, b: {}, c: {}".format(self.a, self.b, self.c)
        return (s)

class testCase(object):
    """This is a class representing a test case result"""
    def __init__(self, filename, name, hostname, time, timestamp, tests, skipped, errors, failures):
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
        s = "filename {}\n".format(self.filename)
        s = s+"time {}".format(self.time)
        s = s + " timestamp {}".format(self.timestamp)
        s = s + " hostname {}".format(self.hostname)
        s = s + " tests {}".format(self.tests)
        s = s + " skipped {}".format(self.skipped)
        s = s + " errors {}".format(self.errors)
        s = s + " failures {}".format(self.failures)
        return (s)

class testResult(object):
    # This is a class representing all test case results from a test.
    # Dictionary of testCase object, with testCase.name.

    def __init__(self, result_directory):
        self.result_directory = result_directory
        self._test_result_hash = dict()
        self.process_test_results()

    def get_results(self):
        return self._test_result_hash

    def process_test_results(self):
        list_XML_files = glob.glob(self.result_directory + "/TEST*.xml")

        # Parse through each xml file.
        for f in list_XML_files:
            tc = self.read_XML_data(f)
            print(tc)
            if tc is not None:
                # Add each testCase into dictionary testResultHash.
                self._test_result_hash[tc.name] = tc

    def read_XML_data(self, filename):
        try:
            # Parse XML data into variables.
            # ET is an imported function called ElementTree.
            tree = ET.parse(filename)
            root = tree.getroot()
            # name = root.attrib.get("name")
            name = "_".join((root.attrib.get("name")).split())
            time = float(root.attrib.get("time"))
            timestamp = root.attrib.get("timestamp")
            hostname = root.attrib.get("hostname")
            tests = int(root.attrib.get("tests"))
            skipped = int(root.attrib.get("skipped"))
            errors = int(root.attrib.get("errors"))
            failures = int(root.attrib.get("failures"))
            # Store results in a testCase.

            tc = testCase(os.path.basename(filename),name,hostname,time,timestamp,tests,skipped,errors,failures)
            return tc
        except Exception as e:
            print("Can not process a file {}".format(filename))
            print(e)
            return None


if __name__ == "__main__":

    # Still need to add check to make sure directory exists
    build_list = os.listdir("/Users/pg/workspace/de/tcprioritization/test-results/master/")
    build_list.sort()
    for f in build_list:
        commit_list = os.listdir("/Users/pg/workspace/de/tcprioritization/test-results/master/"+f)
        commit_list.sort()
        for ff in commit_list:
            print ("/Users/pg/workspace/de/tcprioritization/test-results/master/"+f+"/"+ff+"/build/test-results/test")
            test_result_directory = "/Users/pg/workspace/de/tcprioritization/test-results/master/"+f+"/"+ff+"/build/test-results/test"
            priority_file_directory = "./temp_all"
            data_file_path = "./agg_data.json"

            test_cases_report = testResult(test_result_directory).get_results()
            for i in test_cases_report.values():
                pk = testPriority()
                pk.process_priority(i, priority_file_directory)
                pk.update_agg(data_file_path, i)
