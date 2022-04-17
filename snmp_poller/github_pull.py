import os
import subprocess

#	git config --global --add safe.directory /home/datadog/ops-neteng-public

os.chdir("/home/datadog/ops-neteng-public")
subprocess.call(["git", "pull"])


