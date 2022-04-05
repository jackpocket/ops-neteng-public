#!/bin/sh

#MANUAL STEPS#
#sudo dpkg --configure -a
#sudo apt-get install git -y
#sudo git clone https://github.com/jackpocket/ops-neteng.git
#EXPORT!!!!! ENV variables

#https://github.com/jackpocket/ops-neteng.git

#Remove anything old or remaining
sudo rm ookla*
sudo apt remove datadog-agent -y
#Run this install script
#sudo apt-get update
sudo apt install ssh -y
sudo apt install curl -y
sudo apt install snmp -y

#Install Datadog Agent
curl -s https://s3.amazonaws.com/dd-agent/scripts/install_script.sh | bash /dev/stdin

#Install relevant integrations
sudo -u dd-agent datadog-agent integration install -t datadog-ping==1.0.2 -r
sudo -u dd-agent datadog-agent integration install -t datadog-speedtest==1.0.0 -r

sudo wget https://install.speedtest.net/app/cli/ookla-speedtest-1.1.1-linux-x86_64.tgz
sudo tar -zxvf ookla-speedtest-1.1.1-linux-x86_64.tgz
sudo cp speedtest* /usr/local/bin/

#Press YES
#sudo -u dd-agent speedtest

#Must copy files now
sudo cp ./snmp_poller/profiles/sophos-xg.yaml /etc/datadog-agent/conf.d/snmp.d/profiles/
sudo cp ./snmp_poller/profiles/brother.yaml /etc/datadog-agent/conf.d/snmp.d/profiles/
sudo cp ./snmp_poller/profiles/zyxel.yaml /etc/datadog-agent/conf.d/snmp.d/profiles/
sudo cp ./snmp_poller/conf/ping/conf.yaml /etc/datadog-agent/conf.d/ping.d/
sudo cp ./snmp_poller/conf/speedtest/conf.yaml /etc/datadog-agent/conf.d/speedtest.d/

sudo systemctl enable datadog-agent
sudo systemctl restart datadog-agent
sudo rm speedtest*

