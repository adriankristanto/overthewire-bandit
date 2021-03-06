import sys
import os
# get the path of utils.py, which is stored in the parent directory
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)) + '/..')

import paramiko
import utils

USERNAME = 'bandit0'
PASSWORD = 'bandit0'

# creating a new ssh client
client = paramiko.SSHClient()

# to prevent unknown host error
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# connect to remote server
print('connecting...\n')
client.connect(hostname=utils.ADDRESS, port=utils.PORT, username=USERNAME, password=PASSWORD)

print('ls -la')
stdin, stdout, stderr = client.exec_command('ls -la')
utils.print_stdout(stdout)

# read the password
print('cat readme')
stdin, stdout, stderr = client.exec_command('cat readme')

# save the output from stdout to be list of strings
# if the original stdout is simply passed to the next two functions, 
# the last function will get the input where the pointer is already at the end of the file
# thus, it won't print out anything
stdout = stdout.readlines()
password = utils.get_password(stdout)
utils.print_stdout(stdout)

# bandit1 password: boJ9jbbUNNfktd78OOpsqOltutMc3MY1
print('bandit1 password: ' + password)

client.close()