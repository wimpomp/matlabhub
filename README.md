# Matlab Hub

Start proxied matlab instances from a webpage using Nginx.

## Prerequisites

Linux with Matlab and Python3

## Installation

edit matlabhub/config.py:

    license_file: 'path_to_license.lic'
    port_range: [10000, 65536]
    matlab-proxy-app: '/opt/matlabhub/venv/bin/matlab-proxy-app'  # path to matlab-proxy-app in venv

edit ExecStart to point to gunicorn in python venv in matlab.service:
    
    ExecStart=/opt/matlabhub/venv/bin/gunicorn --bind unix:/tmp/matlabhub.sock matlabhub.app:app

install:

    sudo apt install nginx screen xvfb
    curl -LsSf https://astral.sh/uv/install.sh | sh
    . .bashrc
    uv venv venv --python 3.11
    . venv/bin/activate
    pip install matlabhub
    sudo cp matlab /etc/nginx/sites-available/
    sudo ln -s /etc/nginx/sites-available/matlab /etc/nginx/sites-enabled/matlab
    sudo cp matlab.service /lib/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable nginx
    sudo systemctl enable matlab
    sudo service nginx start
    sudo service matlab start

## Configuration

Change the user, path to the socket file and the port (default: 8585) in matlab and matlab.service.

## Usage

Browse to http://127.0.0.1:8585
