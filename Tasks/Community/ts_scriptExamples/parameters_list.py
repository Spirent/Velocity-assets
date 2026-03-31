import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--debug_level', action='store', dest='debug_level', help='debug_level')
parser.add_argument('--testCaseSpecificParameter', action='store', dest='specificParam', help='just for this script')

results, unknown = parser.parse_known_args()

print("[INFO] Param debug_level from defaultData: " + results.debug_level)
print("[INFO] Param testCaseSpecificParameter from fileNameMatch: " + results.specificParam)
print("[INFO] All arguments: " + str(sys.argv[1:]))
