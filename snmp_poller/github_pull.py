import os
import subprocess

#	git config --global --add safe.directory /home/datadog/ops-neteng-public

os.chdir("/home/datadog/ops-neteng-public")
result = subprocess.check_output(["sudo", "git", "pull"])

coolresult = (str(result))

if "Already up to date." in coolresult:
    print("No updates")
else:
    print("Need need to execute the installer")
    os.system('python3 /home/datadog/ops-neteng-public/snmp_poller/snmp_poller_installer.py')

#test

