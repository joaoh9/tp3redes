nano /etc/apt/sources.list
deb http://archive.ubuntu.com/ubuntu/ bionic main restricted
deb http://security.ubuntu.com/ubuntu/ bionic-security main restricted
deb http://archive.ubuntu.com/ubuntu/ bionic-updates main restricted
deb http://archive.ubuntu.com/ubuntu bionic main universe
deb http://archive.ubuntu.com/ubuntu bionic-security main universe 
deb http://archive.ubuntu.com/ubuntu bionic-updates main universe
sudo apt-get update
sudo apt-get --fix-missing

sudo apt-get install git
git init
git clone
git config --global user.email "joaoh9.costa@gmail.com"
git config --global user.name "joaoh9"
ssh-keygen -t rsa

sudo apt-get install python3-pip
sudo pip3 install virtualenv
sudo apt-get install python3-venv
python3 -m venv venv
. venv/bin/activate
pip3 install Flask

instalar vscode

