from paramiko import SSHClient #pip install these
from scp import SCPClient
dir = "/home/mcgreen/mcgreen2_ws/src/mcgreen_control"#put in directory for mcgreen folder on nuc
host = "upper_pi"
port = 22
username = "upperpi"
password = "mcgreen" # not sure about this
rm_dir = "~/upper_ws/src/mcgreen_control"#put in directory for mcgreen folder on upperpi
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(host, port, username, password)
scp = SCPClient(ssh.get_transport())
scp.put(dir, recursive = True, remote_path = rm_dir)
# Uploading the 'test' directory with its content in the
# '/home/user/dump' remote directory
#scp.put('test', recursive=True, remote_path='/home/user/dump')
scp.close()
host = "lower_pi"
port = 22
username = "lowerpi"
password = "mcgreen" # not sure about this
rm_dir = "~/lower_ws/src/mcgreen_control" #put in directory for mcgreen folder on lowerpi
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(host, port, username, password)
scp = SCPClient(ssh.get_transport())
scp.put(dir, recursive = True, remote_path = rm_dir)
scp.close()
