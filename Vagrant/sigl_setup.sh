#!/bin/bash

echo "Setting up SIGL codebase..."

echo "Installing SPADE..."
sudo add-apt-repository -y ppa:openjdk-r/ppa
sudo apt-get update
sudo apt-get install -y openjdk-11-jdk
sudo apt-get install -y auditd bison clang cmake curl flex fuse git ifupdown libaudit-dev libfuse-dev linux-headers-`uname -r` lsof pkg-config unzip uthash-dev

git clone https://github.com/zeerakb1/SPADE.git
cd SPADE/
git checkout version-process

./configure
make

bin/installPostgres
make KERNEL_MODULES=true
sudo chmod ug+s `which auditctl`
sudo chmod ug+s `which iptables`
sudo chmod ug+s `which kmod`
sudo chown root bin/spadeAuditBridge
sudo chmod ug+s bin/spadeAuditBridge

# Changing active = no to yes
echo "Changing active var value..."
sudo sed -i '/^active =/s/=.*/= yes/' /etc/audisp/plugins.d/af_unix.conf

sudo service auditd restart

echo "Installing Graphviz..."
sudo apt install graphviz -y

echo "Setting up scripts for SIGs"
cd /home/vagrant
git clone https://github.com/zeerakb1/SIGL-scripts.git

echo "Installing dependencies for SIGL"
sudo apt update -y && sudo apt upgrade -y
sudo apt install python3.8 -y
sudo apt update -y

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
echo -e "2\n" | sudo update-alternatives --config python3
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2
echo -e "2\n" | sudo update-alternatives --config python

python3 -m pip install --upgrade pip
sudo apt install python3-pip -y
pip3 install --upgrade pip
sudo apt update -y

pip3 install --upgrade cython
sudo apt-get install python3-numpy -y
#pip3 install numpy
pip3 install jenkspy
pip3 install stellargraph
pip3 install tensorflow==2.11.0
pip3 install keras==2.11.0

git clone https://github.com/IbrahimSanaullah/SIGL.git

