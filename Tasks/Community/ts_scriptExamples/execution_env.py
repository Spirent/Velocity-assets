import os
import textwrap

cwd = os.getcwd()
print()
print('cwd: '+cwd)
print()
print(textwrap.fill('files: '+str(os.listdir(cwd)),width=125))
print()
print(textwrap.fill('environment: '+str(os.environ),width=125))
