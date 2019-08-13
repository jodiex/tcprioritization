import os
import xml.etree.ElementTree as ET
import glob
import json


def isDirectoryValid(resultdirectory):
    # Check if resultdirectory is valid
    if (os.path.isdir(resultdirectory)):
        if not os.listdir(resultdirectory):
            print ("Empty directory.")
            return False
        else:
            return True
    else:
        print ("Directory is invalid.")
        return False
def isPass(test_case):
    if (test_case.failures > 0) or (test_case.skipped > 0) or (test_case.errors > 0):
        return False
    else:
        return True

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
        #print("test cases {}".format(test_case.name))

        self.name = test_case.name
        self.filename = priority_file_name

    def calculate_priority(self, test_case):
        self.totalExecutions = self.totalExecutions + 1
        if (test_case.failures > 0) or (test_case.skipped > 0) or (test_case.errors > 0):
            self.totalFailures = self.totalFailures + 1
            recentFail = 5000
        else:
            recentFail = 0
            self.totalPasses = self.totalPasses + 1
        
        # prevPrioritytemp = self.prevPriority
        self.prevPriority = self.priority
        #print("\nprev value {}".format(self.prevPriority))
        # if test fails on first run, prevent division by zero
        if self.totalPasses == 0:
            recentFail = 5000
            failRatio = 1
        else:
            failRatio = self.totalFailures / self.totalPasses

        priority_value = (self.a * failRatio) + (self.b * self.prevPriority) + recentFail
        #print("\nnew value {}".format(priority_value))
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

        #print ("tpriority.filename {}".format(self.filename))
        # update <testcase>.json file
        jsonFile = open(self.filename, "w+")
        jsonFile.write(json.dumps(priorityJSON))
        jsonFile.close()

    def create_empty_agg_data(self, id):
        aggJSON = {
            "id": id,
            "name": [],
            "failRatio": [],
            "priority": [],
            "pass": []
        }
        return aggJSON

    def load_json_data(self, file_name, mode="r"):
        try:
            data = open(file_name, mode) # Open the data JSON file for reading
            dataFile = json.load(data) # Read the JSON into the buffer
            data.close()
        except Exception as e:
            #print ("loading json: {}".format(str(e)))
            return None
        return dataFile


    def update_agg(self, data_file_path, test_case, commit, pipeline, run, count):
        dataFile = self.load_json_data(data_file_path)
        if dataFile is None:
            # print("\n\n\ndataFile is None\n\n\n")
            dataFile = dict()
            id = str(commit) + "_" + str(pipeline) + "_" + str(run)
            dataFile = self.create_empty_agg_data(id)

        if test_case.name not in dataFile['name']:
            # print("can not find in file {}".format(tc.filename))
            dataFile['name'].append(test_case.name)
            if self.totalPasses is not 0:
                failRatio = self.totalFailures / self.totalPasses
            else:
                failRatio = 1
            dataFile['failRatio'].append(failRatio)
            dataFile['priority'].append(self.priority)
            passfail = isPass(test_case)
            dataFile['pass'].append(passfail)
            # print("Datafile: {}".format(dataFile))

            # write data to JSON aggregate data file
            data = open(data_file_path, "w+")
            data.write(json.dumps(dataFile))
            data.close()

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
            #print(tc)
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

            base = os.path.basename(filename)
            filename = os.path.splitext(base)[0]

            tc = testCase(filename,name,hostname,time,timestamp,tests,skipped,errors,failures)
            return tc
        except Exception as e:
            print("Can not process a file {}".format(filename))
            print(e)
            return None


if __name__ == "__main__":
    
    #build_list = os.listdir("/Users/pg/workspace/de/tcprioritization/test-results/master/")
    #build_list.sort()
    #for f in build_list:
    commit = 1234567
    pipeline_list = os.listdir("/Users/jxiang/Documents/TCP/test_result1/"+str(commit))
    priority_file_directory = "/Users/jxiang/Documents/TCP/JSON2/"
    data_file_path = "/Users/jxiang/Documents/TCP/agg2.json"
    count = 0

    for f in pipeline_list:
        run_list = os.listdir("/Users/jxiang/Documents/TCP/test_result1/"+str(commit)+"/"+f)
        for ff in run_list:
            test_result_directory = "/Users/jxiang/Documents/TCP/test_result1/"+str(commit)+"/"+f+"/"+ff+"/acceptanceTestsResults/test"
            if isDirectoryValid(test_result_directory):
                test_cases_report = testResult(test_result_directory).get_results()
                for i in test_cases_report.values():
                    pk = testPriority()
                    pk.process_priority(i, priority_file_directory)
                    pk.update_agg(data_file_path, i, commit, f, ff, count)
                    count = count + 1


    # get name of build, store it in tc, agg_Data
    # check if pipeline has acceptanceTestsResults folder