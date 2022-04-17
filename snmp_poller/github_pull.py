import os
import subprocess

#	git config --global --add safe.directory /home/datadog/ops-neteng-public

os.chdir("/home/datadog/ops-neteng-public")
subprocess.call(["sudo", "git", "pull"])
result = subprocess.check_output(["sudo", "git", "pull"])
print(result)

