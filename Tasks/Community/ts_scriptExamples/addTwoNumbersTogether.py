import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-input_number1', action='store', dest='number1', help='1st number')
parser.add_argument('-input_number2', action='store', dest='number2', help='2nd number')

results, unknown = parser.parse_known_args()

added = int(results.number1) + int(results.number2)
subtracted = int(results.number1) - int(results.number2)
print("[INFO] Param number1: " + results.number1)
print("[INFO] Param number2: " + results.number2)
print("Added: " + str(added))
print("Subtracted: " + str(subtracted))
print("Finished: PASSED")
