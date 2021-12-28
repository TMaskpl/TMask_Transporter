hostname = ''
username = ''
# key_filename='/home/Python/.ssh/id_rsa
password = ''
port = 22

ssh_path = '/home/Python/bkp'
command = "ls -l /home/Python/bkp | awk -F ' ' '{print $9, $5}'"
# list_remote_files = "ls -l /home/Python/bkp | awk -F ' ' '{print $9}'"
list_remote_files = "ls -1 /home/Python/bkp"
