import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--text', action='store', dest='text')
parser.add_argument('--boolean', action='store', dest='boolean')
parser.add_argument('--double', action='store', dest='double')
parser.add_argument('--integer', action='store', dest='integer')
parser.add_argument('--custom', action='store', dest='custom')

results, unknown = parser.parse_known_args()

print("[INFO] Text: " + results.text)
print("[INFO] Boolean: " + results.boolean)
print("[INFO] Double: " + str(results.double))
print("[INFO] Integer: " + str(results.integer))
print("[INFO] Custom: " + results.custom)
print("[INFO] All arguments: " + str(sys.argv[1:]))
