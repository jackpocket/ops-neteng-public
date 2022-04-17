import os
import subprocess

#	git config --global --add safe.directory /home/datadog/ops-neteng-public

# os.chdir("/home/datadog/ops-neteng-public")
# result = subprocess.check_output(["sudo", "git", "pull"])

p = subprocess.Popen("pwd", stdout=subprocess.PIPE)
result = p.communicate()[0]
print result


# if "Already up to date." in result:
#     print("No updates")
# else:
#     print("Need need to execute the installer")


#test

