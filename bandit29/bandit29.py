import os
import sys
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)) + '/..')

import paramiko
import utils
import time
import uuid

USERNAME = 'bandit29'
PASSWORD = 'bbc96594b4e001778eee9975372716b2'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print('connecting...\n')
client.connect(hostname=utils.ADDRESS, port=utils.PORT, username=USERNAME, password=PASSWORD)

FOLDERNAME = str(uuid.uuid4())
REPONAME = 'ssh://bandit29-git@localhost/home/bandit29-git/repo'
print(f'folder name: {FOLDERNAME}\n')

print(f"mkdir /tmp/{FOLDERNAME} && cd /tmp/{FOLDERNAME} && git clone {REPONAME}")
stdin, stdout, _ = client.exec_command(f"mkdir /tmp/{FOLDERNAME} && cd /tmp/{FOLDERNAME} && git clone {REPONAME}", get_pty=True)
time.sleep(1)
stdin.write('yes\n')
time.sleep(1)
stdin.write(PASSWORD + '\n')
stdin.flush()
utils.print_stdout(stdout)

print(f"cat /tmp/{FOLDERNAME}/repo/README.md")
_, stdout, _ = client.exec_command(f"cat /tmp/{FOLDERNAME}/repo/README.md")
utils.print_stdout(stdout)
# from the above command, we can read README.md, which shows that 
# there is no password in production branch or the master branch
# which might suggest the existence of a development branch

# reference: https://www.jquery-az.com/list-branches-git/
# to list all branches in local and remote repositories, we can use 
# git branch -a
print(f"cd /tmp/{FOLDERNAME}/repo && git branch -a")
_, stdout, _ = client.exec_command(f"cd /tmp/{FOLDERNAME}/repo && git branch -a")
utils.print_stdout(stdout)
# we found out that there is a "dev" branch, which we can check out

print(f"cd /tmp/{FOLDERNAME}/repo && git checkout dev")
_, stdout, _ = client.exec_command(f"cd /tmp/{FOLDERNAME}/repo && git checkout dev")
utils.print_stdout(stdout)

print(f"cat /tmp/{FOLDERNAME}/repo/README.md")
_, stdout, _ = client.exec_command(f"cat /tmp/{FOLDERNAME}/repo/README.md")
stdout = stdout.readlines()
utils.print_stdout(stdout)

password = stdout[-2].split()[-1]
# bandit30 password: 5b90576bedb2cc04c86a9e924ce42faf
print(f'bandit30 password: {password}\n')

# ALTERNATIVE METHOD: 
# read paked-refs file in .git directory
# which contains all mapping to branches and tags
# we can use git show <commit hash> into the dev branch

# clean up
print('deleting temporary directory...')
client.exec_command(f'rm -rf /tmp/{FOLDERNAME}')

client.close()