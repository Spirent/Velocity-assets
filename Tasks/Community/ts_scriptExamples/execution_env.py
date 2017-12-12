import os
cwd = os.getcwd()
print('\ncwd: '+cwd)
print('\nfiles: '+str(os.listdir(cwd)))
print('\nenvironment: '+str(os.environ))
