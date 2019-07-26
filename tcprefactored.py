import os
import xml.etree.ElementTree as ET
import glob
import json
import sys

#todo Do we need this?
def isDirectoryValid(resultdirectory):
    """check if resultdirectory is valid"""
    if (os.path.isdir(resultdirectory)):
        if not os.listdir(resultdirectory):
            print ("Empty directory.")
            return False
        else:
            return True
    else:
        print ("Directory is invalid.")
        return False


def write_to_json(self, data_file_path, data_file):
    data = open(data_file_path, "w+")
    data.write(json.dumps(data_file))
    data.close()

# todo need to consider how to take care of a modified test case

class testPriority(object):
    """This is a class representing the priority data of a test case result"""
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

    def __init__(self, priority_dict=None):
        if priority_dict:
            self._set_priority(priority_dict)

    def _set_priority(self, priority_dict):
        self.name = priority_dict['name']
        self.prevPriority = priority_dict['prevPriority']
        self.priority = priority_dict['priority']
        self.totalExecutions = priority_dict['totalExecutions']
        self.totalFailures = priority_dict['totalFailures']
        self.totalPasses = priority_dict['totalPasses']

    def process_priority(self, test_case, priority_file_directory):
        self.update_priority_from_file(test_case, priority_file_directory)
        self.calculate_priority(test_case)
        self.update_priority()

    def update_priority_from_file(self, test_case, priority_file_directory):
        # find matching JSON file and get JSON data
        priority_file_name = priority_file_directory + test_case.filename + '.json'

        if os.path.exists(priority_file_name): # check for an existing JSON file
            json_file = open(priority_file_name, "r") # Open the JSON file for reading
            priority_dict = json.load(json_file) # Read the JSON into the buffer
            json_file.close()
            self._set_priority(priority_dict)
        print("test cases {}".format(test_case.name))

        self.name = test_case.name
        self.filename = priority_file_name

    def calculate_priority(self, test_case):
        # check if testCase and testPriority are valid
        # priority_value = 1000
        if test_case:
            self.totalExecutions = self.totalExecutions + test_case.tests
            self.totalFailures = self.totalFailures + test_case.failures

            if test_case.failures > 0:
                recentFail = 5000
            else:
                recentFail = 0

            # take error into account
            tcPasses = test_case.tests - test_case.failures
            if tcPasses < 0:
                tcPasses = 0
            self.totalPasses = self.totalPasses + tcPasses
            # prevPrioritytemp = self.prevPriority
            self.prevPriority = self.priority
            print("\nprev value {}".format(self.prevPriority))
            # if test fails on first run, prevent division by zero
            if self.totalPasses == 0:
                recentFail = 5000
                failRatio = 0
            else:
                failRatio = self.totalFailures / self.totalPasses

            priority_value = (self.a * failRatio) + (self.b * self.prevPriority) + recentFail
            print("\nnew value {}".format(priority_value))
            if priority_value < 0.00001: # prevent priority values from getting infinitely small
                priority_value = 0
        self.priority = priority_value

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
            "totalPasses": self.totalPasses
        }

        print ("tpriority.filename {}".format(self.filename))
        # update <testcase>.json file
        write_to_json(self.filename, priorityJSON)

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

            write_to_json(data_file_path, data_file)
        except Exception as e: # if file is empty
            # print('create_new_agg_tc: '+str(e))
            write_to_json(data_file_path, agg_json)

    def update_agg(self, data_file_path, test_case):
        data_file = self.load_json_data(data_file_path)
        if data_file is None:
            # print("\n\n\ndataFile is None\n\n\n")
            data_file = dict()

        if test_case.filename not in data_file:
            # print("can not find in file {}".format(tc.filename))
            new_agg_data = self.create_empty_agg_data(test_case.filename)
            data_file.update(new_agg_data)
            # print("Datafile: {}".format(dataFile))

        try: # if test case exists in aggregate data file
            # append new values to end of arrays
            data_file[test_case.filename]['timestamp'].append(test_case.timestamp)
            data_file[test_case.filename]['priorityval'].append(self.priority)
            if self.totalPasses is not 0:
                failRatio = self.totalFailures / self.totalPasses
            else:
                failRatio = 0
            data_file[test_case.filename]['passfail'].append(failRatio)

            # write data to JSON compiled data file
            write_to_json(data_file_path, data_file)
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
    """This is a class representing all test case results from a test"""
    # dictionary of testCase object, with testCase.name

    def __init__(self, result_directory):
        #todo sanitize result directory; make sure if valid, etc
        self.result_directory = result_directory
        self._test_result_hash = dict()
        self.process_test_results()

    def get_results(self):
        return self._test_result_hash

    def process_test_results(self):
        list_XML_files = glob.glob(self.result_directory + "/*.xml")

        for f in list_XML_files:
            tc = self.read_XML_data(f)
            print(tc)
            if tc is not None:
                # add each testCase into dictionary testResultHash
                self._test_result_hash[tc.name] = tc

    def read_XML_data(self, filename):
        try:
            # get filename of each XML file
            # parse XML data into variables
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
            # store results in a testCase

            tc = testCase(os.path.basename(filename),name,hostname,time,timestamp,tests,skipped,errors,failures)
            return tc
        except Exception as e:
            print("Can not process a file {}".format(filename))
            print(e)
            return None


if __name__ == "__main__":
    # test_result_directory = "./temp"
    # priority_file_directory = "./temp_out/"
    # data_file_path = "./agg_data_small.json"
    # test_cases_report = testResult(test_result_directory)
    # for i in test_cases_report._test_result_hash.values():
    #     pk = testPriority()
    #     pk.process_priority(i, priority_file_directory)
    #     pk.update_agg(data_file_path, i)
    #     print(pk)
    #     print("\n")
    #
    #run all
    
    
    # build_list = os.listdir("/Users/pg/workspace/de/tcprioritization/test-results/master/")
    master_path = sys.argv[1]
    build_list = os.listdir(master_path)
    build_list.sort()
    for f in build_list:
        # commit_list = os.listdir("/Users/pg/workspace/de/tcprioritization/test-results/master/"+f)
        commit_list = os.listdir(master_path+f)
        commit_list.sort()
        for ff in commit_list:
            #print ("/Users/pg/workspace/de/tcprioritization/test-results/master/"+f+"/"+ff+"/build/test-results/test")
            test_result_directory = master_path+f+"/"+ff+"/build/test-results/test"
            # priority_file_directory = "./temp_all/"
            priority_file_directory = sys.argv[2]
            # data_file_path = "./agg_data.json"
            data_file_path = sys.argv[3]

            test_cases_report = testResult(test_result_directory).get_results()
            for i in test_cases_report.values():
                pk = testPriority()
                pk.process_priority(i, priority_file_directory)
                pk.update_agg(data_file_path, i)