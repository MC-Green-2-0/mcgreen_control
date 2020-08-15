from paramiko import SSHClient
from scp import SCPClient

cmdu = "rm -r ~/upper_ws/src/mcgreen_control/"
cmdl = "rm -r ~/lower_ws/src/mcgreen_control/"
dir = "/home/mcgreen/mcgreen2_ws/src/mcgreen_control"

host = "upper_pi"
port = 22
username = "upperpi"
password = "mcgreen"
rm_dir = "~/upper_ws/src"

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(host, port, username, password)

(ssh_stdin, ssh_stdout, ssh_stderr) = ssh.exec_command(cmdu)
ssh.close()
del ssh_stdin, ssh_stdout, ssh_stderr

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(host, port, username, password)

scp = SCPClient(ssh.get_transport())
scp.put(dir, recursive = True, remote_path = rm_dir)

scp.close()
ssh.close()

host = "lower_pi"
port = 22
username = "lowerpi"
password = "mcgreen"
rm_dir = "~/lower_ws/src"

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(host, port, username, password)

(ssh_stdin, ssh_stdout, ssh_stderr) = ssh.exec_command(cmdl)
ssh.close()
del ssh_stdin, ssh_stdout, ssh_stderr

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(host, port, username, password)

scp = SCPClient(ssh.get_transport())
scp.put(dir, recursive = True, remote_path = rm_dir)

scp.close()
ssh.close()
