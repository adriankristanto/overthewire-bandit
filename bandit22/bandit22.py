import os
import sys
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)) + '/..')

import utils
import paramiko

USERNAME = 'bandit22'
PASSWORD = 'Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print('connecting...\n')
client.connect(hostname=utils.ADDRESS, port=utils.PORT, username=USERNAME, password=PASSWORD)

print('ls -l /etc/cron.d')

# read the cronjob of bandit23
print('cat /etc/cron.d/cronjob_bandit23')

# read the executed script
print('cat /usr/bin/cronjob_bandit23.sh')

# firstly, the script would generate the md5 hash of the 
# sentence: "I am user $myname"
# since we are trying to get the password of bandit23, we can replace $myname with bandit23
# then we get the md5 hash of the sentence "I am user bandit23" with
# echo I am user bandit23 | md5sum | cut -d ' ' -f 1
# because md5sum would output: 8ca319486bfbbc3663ea0fbe81326349  -
# and we only want the first column
# finally, we know that the filename is the md5 hash stored in the tmp directory,
# we can make it into a variable and read it immediately
print("cat /tmp/$(echo I am user bandit23 | md5sum | cut  -d ' ' -f 1)")

client.close()