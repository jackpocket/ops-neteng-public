Step1. Build a Hyper-V ubuntu server VM
Step2. Login to VM, set environment variables and check out repo
Step3. Run the installer
Step4. A few manual steps to make sure we have "automation"

REQUIRED - Place all required environment variables into /etc/environment:

sudo git clone https://github.com/jackpocket/ops-neteng-public.git

cd ops-neteng-public

python3 snmp_poller/snmp_poller

add cronjob
add line to /etc/sudoers

CHECKS:
sudo -u dd-agent datadog-agent check snmp
sudo -u dd-agent datadog-agent check agent
sudo -u dd-agent datadog-agent check speedtest
sudo -u dd-agent datadog-agent check ping
sudo -u dd-agent datadog-agent check tcp_check
