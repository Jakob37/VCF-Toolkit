Bootstrap: docker
From: python:3

%post
    apt-get -y update
    apt-get -y install git-all python3-pip python3.11-venv
    git clone https://github.com/Jakob37/My-VCF-tools
    python3 -m venv .venv
    . .venv/bin/activate
    ls
    pwd
    python3 -m pip install -r My-VCF-tools/requirements.txt

%environment
    export LC_ALL=C

%runscript
    My-VCF-tools/vtk

