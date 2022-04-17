import os
import subprocess

#	git config --global --add safe.directory /home/datadog/ops-neteng-public

subprocess.Popen("cd", cwd="/home/datadog/ops-netng-public")
subprocess.call(["git", "pull"])


