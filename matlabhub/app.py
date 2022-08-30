import os
import sys
import re
import socket
import subprocess
import random
import yaml
from flask import Flask, redirect, render_template, request
from time import sleep

with open(os.path.join(os.path.dirname(__file__), 'config.yml')) as conf_file:
    config = yaml.safe_load(conf_file)


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


class Matlab:
    def __init__(self, port, group=None):
        self.port = int(port)
        self.group = group
        self.screen_name = f'matlab_{port}' if group is None else f'matlab_{group}_{port}'

    def start(self):
        command = f'screen -S {self.screen_name} -d -m env MWI_BASE_URL="/{self.port}" ' \
                  f'MWI_APP_PORT={self.port} MLM_LICENSE_FILE={config["license_file"]} matlab-proxy-app'
        subprocess.Popen(command, shell=True, start_new_session=True)

    def stop(self):
        subprocess.run(f"screen -S {self.screen_name} -X stuff '^C'", shell=True)


class Hub(dict):
    def __init__(self):
        super().__init__()
        self.update({matlab.port: matlab for matlab in self.find_running()})

    @staticmethod
    def find_running():
        p = subprocess.run('screen -list', shell=True, capture_output=True)
        return [Matlab(port, group) for group, port in re.findall(r'\.matlab_([^_]+)_(\d+)', str(p.stdout))]

    def new(self, group=None):
        group = re.escape(re.sub(r'\W|_', '', group))
        ports = list(range(*config['port_range']))
        random.shuffle(ports)
        for port in ports:
            if port not in self and not is_port_in_use(port):
                self[port] = Matlab(port, group)
                self[port].start()
                sleep(5)
                return redirect(f'/{port}')

    def stop(self, port):
        self.pop(port).stop()

    def get_groups(self):
        return list(set(matlab.group for matlab in self.values()))

    def get_ports(self, group=None):
        return [matlab.port for matlab in self.values() if matlab.group == group]


sys.argv = sys.argv[:1]
hub = Hub()
app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/default')


@app.route('/<group>')
def group(group):
    return render_template('index.html', ports=hub.get_ports(group), groups=hub.get_groups(), group=group)


@app.route('/<group>/start/new')
def group_start_new(group):
    return hub.new(group)


@app.route('/<group>', methods=['POST'])
def start_new_post(group):
    return hub.new(request.form['group'])


@app.route('/<group>/stop/<port>')
def stop(group, port):
    hub.stop(int(port))
    return redirect(f'/{group}')
