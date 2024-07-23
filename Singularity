Bootstrap: docker
From: python:3.11

%post
    apt-get -y update
    apt-get -y install git-all python3-pip python3.11-venv tabix bsdmainutils
    git clone https://github.com/Jakob37/My-VCF-tools
    python3 -m venv /opt/venv
    . /opt/venv/bin/activate
    python3 -m pip install -r My-VCF-tools/requirements.txt

%environment
    export LC_ALL=C
    export PATH="/opt/venv/bin:$PATH"

%runscript
    #!/bin/bash
    source /opt/venv/bin/activate
    python3 /My-VCF-tools/vtk
