import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--build', action='store', dest='build', help='build number')
parser.add_argument('--testCaseSpecificParameter', action='store', dest='specificParam', help='just for this script')

results, unknown = parser.parse_known_args()

print("[INFO] Param build from defaultData: " + results.build)
print("[INFO] Param testCaseSpecificParamer from fileNameMatch: " + results.specificParam)
print("[INFO] All arguments: " + str(sys.argv[1:]))
