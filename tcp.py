import os
import xml.etree.ElementTree as ET
import glob

class testPriority(object):
    # name: "Edit assignment",
    # prevPriority: 0.5,
    # priority: 0.03
    # totalExecutions: 12342,
    # totalFailures: 0,
    # totalPasses: 345,
    pass

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
            s = s + "timestamp {}".format(self.timestamp)
            s = s + "tests {}".format(self.tests)
            s = s + "skipped {}".format(self.skipped)
            s = s + "errors {}".format(self.errors)
            s = s + "failures {}".format(self.failures)
            return (s)

class testResult(object):
    #This is a class representing a test result
    resultdirectory = None
    timestamp = None
    hostname = None
    testPriorityFile = None
    #dictionary of testCase object, with testCase.name 
    test_case = {}
  
    def _init_(self, resultdirectory):
        #check if resultdirectory is valid
        #create database connection
        pass

    # def _init_(self, resultdirectory, testPriorityFile):
    #     #check if resultdirectory is valid
    #     #check if testPriorityFile exist and has permission to write
    #     pass

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


def calculatePriority(testCase):
    pass

def temp(resultdirectory):
    #how to check if resultdirectory is valid
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
            # tree = ET.parse(resultdirectory + "/test1.xml")
    
            #parse line into variables 
            name = root.attrib.get("name")
            time = root.attrib.get("time")
            timestamp = root.attrib.get("timestamp")
            tests = root.attrib.get("tests")
            skipped = root.attrib.get("skipped")
            errors = root.attrib.get("errors")
            failures = root.attrib.get("failures")
            tc = testCase(name,time,timestamp,tests,skipped,errors,failures)
            #store tc in an array
            testResultHash[tc.name] = tc
        except Exception as e:
            print ("ops! can not process a file {}".format(x))
            print (e)
            print(len(x))
            # f = open(x, "r")
            # print(f.read())
            # f.close()

    # file1 = '/Users/jxiang/Downloads/build/build/test-results/test2/TEST-Scenario#3a#20Successfully#20create#20a#20lesson#20with#20limited#20#22How#20Did#20I#20Do#3f#22s#20and#20an#20algorithmic#20question#2c#20and#20confirm#20that#20#22Try#20Another#22#20resets#20the#20#22How#20Did#20I#20Do#3f#22#20counter.xml'
    # f = open(file1, "r")
    # print(f.read())
    # f.close()
    # for n, o in testResultHash.items():
    #     print ("test {} => {}".format(n, o))
    print ("total test cases {}".format(len(testResultHash)))
        
        


if __name__ == "__main__":
    print("This is main...")
    #temp("C:/Users/jxiang/Downloads/test-result-28june-build/test-results/test")
    # temp("./test1")
    # temp("\\?\C:\Users\jxiang\Downloads\build\build\test-results\test2")
    #temp("/Users/jxiang/Downloads/build/build/test-results/test2")
    # t1 = testResult("testfile", "outfile")
    # t1.get_data_from_file()
    # t1.write_data_to_priority()

