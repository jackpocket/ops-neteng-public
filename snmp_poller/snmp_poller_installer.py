import os
import fileinput
import subprocess

#os.system('sudo apt remove -y datadog-agent')
os.system('sudo systemctl stop datadog-agent')

#TODO this does not work - using source is the only option
#os.system('source /etc/environment')
#TODO moving this to a manual step for now

# Get DD environment variables
dd_api_key = os.getenv('DD_API_KEY')
dd_agent_major_version = os.getenv('DD_AGENT_MAJOR_VERSION')
dd_install_only = os.getenv('DD_INSTALL_ONLY')
dd_weburl = os.getenv('DD_WEBURL')

# Get JP environment variables
site = os.getenv('SITE')
snmp_user = os.getenv('SNMP_USER')
comm_string = os.getenv('COMM_STRING')
auth_key = os.getenv('AUTH_KEY')
priv_key = os.getenv('PRIV_KEY')
firewall_ip = os.getenv('FIREWALL_IP')  # LOCATE DEFAULT GW
network_management_subnet = os.getenv('NETWORK_MANAGEMENT_SUBNET')
printer_vlan = os.getenv('PRINTER_VLAN')
upload_ftp_prod = os.getenv('UPLOAD_FTP_PROD')


# Update - slow
# os.system('sudo apt update')

# disable ipv6
os.system('sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1')
os.system('sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1')
os.system('sudo sysctl -w net.ipv6.conf.lo.disable_ipv6=1')

# Install some packages
try:
    os.system('sudo apt install -y ssh')
    os.system('sudo apt install -y iputils-ping')
    os.system('sudo apt install -y curl')
    os.system('sudo apt install -y snmp')
    os.system('sudo apt install -y net-tools')
    os.system('sudo apt install -y syslog-ng')

except:
    exit("Failed to install the packages")

# Install Datadog Agent - hope this does not change
os.system('curl -s https://s3.amazonaws.com/dd-agent/scripts/install_script.sh | bash /dev/stdin')

# Install relevant integrations
os.system('sudo -u dd-agent datadog-agent integration install -t datadog-ping==1.0.2 -r')
os.system('sudo -u dd-agent datadog-agent integration install -t datadog-speedtest==1.0.0 -r')

# Install speedtest utility
os.system('sudo wget https://install.speedtest.net/app/cli/ookla-speedtest-1.1.1-linux-x86_64.tgz')
os.system('sudo tar -zxf ookla-speedtest-1.1.1-linux-x86_64.tgz')
os.system('sudo cp speedtest* /usr/local/bin/')

# Copy templated files
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/profiles/sophos-xg.yaml /etc/datadog-agent/conf.d/snmp.d/profiles/')
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/profiles/brother.yaml /etc/datadog-agent/conf.d/snmp.d/profiles/')
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/profiles/zyxel.yaml /etc/datadog-agent/conf.d/snmp.d/profiles/')
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/profiles/eaton.yaml /etc/datadog-agent/conf.d/snmp.d/profiles/')
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/conf/ping/conf.yaml /etc/datadog-agent/conf.d/ping.d/')
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/conf/speedtest/conf.yaml /etc/datadog-agent/conf.d/speedtest.d/')
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/conf/tcp_check/conf.yaml /etc/datadog-agent/conf.d/tcp_check.d/')
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/conf/snmp/conf.yaml /etc/datadog-agent/conf.d/snmp.d/')
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/conf/agent/datadog.yaml /etc/datadog-agent/')
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/conf/syslog-ng/sophos.conf /etc/syslog-ng/conf.d/')

os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/github_pull.py /opt/')
os.system('sudo chmod +x /opt/github_pull.py')

# Give each file a variable
dd_agent_conf = '/etc/datadog-agent/datadog.yaml'
dd_snmp_conf = '/etc/datadog-agent/conf.d/snmp.d/conf.yaml'
dd_ping_conf = '/etc/datadog-agent/conf.d/ping.d/conf.yaml'
dd_speedtest_conf = '/etc/datadog-agent/conf.d/speedtest.d/conf.yaml'
dd_tcp_check_conf = '/etc/datadog-agent/conf.d/tcp_check.d/conf.yaml'

# Replace vars in files
# with fileinput.FileInput(dd_snmp_conf, inplace=True, backup='.bak') as myfile:
#
# with fileinput.FileInput(dd_snmp_conf, inplace=True) as myfile:
#     for line in myfile:
#         #print(line.replace('<SITE>', site), end='')
#         print(line.replace('<SITE>', site))
#         print(line.replace('<COMM_STRING>', comm_string))
#         print(line.replace('<AUTH_KEY>', auth_key))
#         print(line.replace('<PRIV_KEY>', priv_key))
#         print(line.replace('<FIREWALL_IP>', firewall_ip))
#         print(line.replace('<NETWORK_MANAGEMENT_SUBNET>', network_management_subnet))
#         print(line.replace('<SNMP_USER>', snmp_user))
#
# with fileinput.FileInput(dd_tcp_check_conf, inplace=True) as myfile:
#     for line in myfile:
#         print(line.replace('<SITE>', site))
#         print(line.replace('<UPLOAD_FTP_PROD>', site))
#
# with fileinput.FileInput(dd_agent_conf, inplace=True) as myfile:
#     for line in myfile:
#         print(line.replace('<SITE>', site))
#         print(line.replace('<DD_API_KEY>', site))
#         print(line.replace('<DD_SITE>', site))
#
# with fileinput.FileInput(dd_ping_conf, inplace=True) as myfile:
#     for line in myfile:
#         print(line.replace('<SITE>', site))
#
# with fileinput.FileInput(dd_speedtest_conf, inplace=True) as myfile:
#     for line in myfile:
#         print(line.replace('<SITE>', site))

#WORKS - callcheck but we do run below
#subprocess.check_output(f'sudo sed -i s/SITE/{site}/g /etc/datadog-agent/conf.d/ping.d/conf.yaml', shell=True)
subprocess.run(f'sudo sed -i s/SITE/{site}/g /etc/datadog-agent/conf.d/ping.d/conf.yaml', shell=True)
subprocess.run(f'sudo sed -i s/SITE/{site}/g /etc/datadog-agent/conf.d/speedtest.d/conf.yaml', shell=True)
subprocess.run(f'sudo sed -i s/SITE/{site}/g /etc/datadog-agent/conf.d/tcp_check.d/conf.yaml', shell=True)
subprocess.run(f'sudo sed -i s/SITE/{site}/g /etc/datadog-agent/conf.d/snmp.d/conf.yaml', shell=True)

subprocess.run(f'sudo sed -i s/SITE/{site}/g /etc/datadog-agent/datadog.yaml', shell=True)
subprocess.run(f'sudo sed -i s/SITE/{site}/g /etc/syslog-ng/conf.d/sophos.conf', shell=True)

subprocess.run(f'sudo sed -i s/DD_WEBURL/{dd_weburl}/g /etc/datadog-agent/datadog.yaml', shell=True)

subprocess.run(f'sudo sed -i s/DD_API_KEY/{dd_api_key}/g /etc/datadog-agent/datadog.yaml', shell=True)
subprocess.run(f'sudo sed -i s/DD_API_KEY/{dd_api_key}/g /etc/syslog-ng/conf.d/sophos.conf', shell=True)

subprocess.run(f'sudo sed -i s/FIREWALL_IP/{firewall_ip}/g /etc/datadog-agent/conf.d/snmp.d/conf.yaml', shell=True)
subprocess.run(f'sudo sed -i s/AUTH_KEY/{auth_key}/g /etc/datadog-agent/conf.d/snmp.d/conf.yaml', shell=True)
subprocess.run(f'sudo sed -i s/PRIV_KEY/{priv_key}/g /etc/datadog-agent/conf.d/snmp.d/conf.yaml', shell=True)
subprocess.run(f'sudo sed -i s/COMMUNITY_STRING/{comm_string}/g /etc/datadog-agent/conf.d/snmp.d/conf.yaml', shell=True)
#sed does not like the slash at the end of the subnet
#network_management_subnet.replace("/", "\/", 1)

if os.getenv('UPS_IP') is None:
    #ups_ip = '127.0.0.1'
    pass
else:
    ups_ip = os.getenv('UPS_IP')
    subprocess.run(f'sudo sed -i s#UPS_IP#{ups_ip}#g /etc/datadog-agent/conf.d/snmp.d/conf.yaml', shell=True)

subprocess.run(f'sudo sed -i s#NETWORK_MANAGEMENT_SUBNET#{network_management_subnet}#g /etc/datadog-agent/conf.d/snmp.d/conf.yaml', shell=True)
subprocess.run(f'sudo sed -i s#PRINTER_VLAN#{printer_vlan}#g /etc/datadog-agent/conf.d/snmp.d/conf.yaml', shell=True)
subprocess.run(f'sudo sed -i s/SNMP_USER/{snmp_user}/g /etc/datadog-agent/conf.d/snmp.d/conf.yaml', shell=True)
subprocess.run(f'sudo sed -i s/UPLOAD_FTP_PROD/{upload_ftp_prod}/g /etc/datadog-agent/conf.d/tcp_check.d/conf.yaml', shell=True)

#Deal wth interface name
#find primary interface. assume there is only one for right now
#find the subnet/vlan, find gateway
#gateway can be used for firewall IP
#subnet can be used for network-management IP

#interface for speedtest is not matching template
#rename it to eth0
#find name of it first
#sudo ifconfig ens160 down && sudo /sbin/ip link set ens160 name eth0 && sudo ifconfig eth0 up

os.system('sudo systemctl enable datadog-agent')
os.system('sudo systemctl restart datadog-agent')
os.system('sudo systemctl restart syslog-ng')
# os.system('sudo apt-get remove --purge lacework -y')
#
# os.system('sudo rm -rf /home/datadog/lacework')

# #Cleanup
os.system('sudo rm speedtest*')
os.system('sudo rm ookla*')
# #Press YES to accept agreement and run the test at least once
# #This must run in order for the check to succeed
os.system('sudo -u dd-agent speedtest')


