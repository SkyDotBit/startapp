from flask import Flask, render_template, request, jsonify, send_file
import json
from websocket_server import WebsocketServer
import asyncio
import subprocess
import threading
import signal
import os
import sys
import psutil
import time
from urllib.parse import urlparse
time.sleep(1)
output_lines = []
clients = []
process = None
websocketport = 8062 # You can change this but it'll break things if you do it incorrectly.
websocket_connection = None
app = Flask(__name__)
with open('config.json', 'r') as j:
    config = json.load(j)

@app.route('/')
def home():
    return render_template('index.html')



def runningquestionmark(app_name):
    for process in psutil.process_iter(['name', 'cmdline']):
        try:
            name = process.info['name'] or ''
            cmdline = process.info['cmdline'] or []
            combined = ' '.join(cmdline).lower()
            if app_name.lower() in name.lower() or app_name.lower() in combined:
                print(f"Found: {name} | {cmdline}")
                return True
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    return False

def newalive(client, server):
    clients.append(client)
    print(f"New client spawned in with ID: {client['id']}")

def clientdead(client, server):
    global clients
    clients.remove(client)
    print(clients)
    print(f"You defeated the client +10xp with ID: {client['id']}")

def send_output_to_clients(output):
    for client in clients:
        server.send_message(client, output)
server = WebsocketServer(host='0.0.0.0', port=6789)
server.set_fn_new_client(newalive)
server.set_fn_client_left(clientdead)
async def execute(command):
    print("Executive man is eating me alive oh please help")
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )

    while True:
        line = await process.stdout.readline()
        if not line:
            break
        decoded_line = line.decode().strip()
        print(decoded_line)
        send_output_to_clients(decoded_line)

    await process.wait()

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coro)

@app.route('/exe')
async def exe():
    print("Exe")
    send_output_to_clients("==========Starting==========")

    if config['args'] != "":
        command = [config['command'], config['args'], config['executablepath']]
    else:
        command = [config['command'], config['executablepath']]
    
    threded = threading.Thread(target=run_async, args=(execute(command),))
    threded.start()
    return 'True'

@app.route('/statusscript')
async def statusscript():
    if runningquestionmark(config['executablepath']):
        return jsonify({"message": "OK"}), 200
    else:
        return jsonify({"message": "NO"}), 100

    
@app.route('/restart')
def restart():
    subprocess.run(f'python cleanup.py "' + config['command'] + f' ' + config['args'] + ' ' + config['executablepath'] + '"', shell=True)
    print("Exe")
    send_output_to_clients("==========Starting==========")

    if config['args'] != "":
        command = [config['command'], config['args'], config['executablepath']]
    else:
        command = [config['command'], config['executablepath']]
    
    threded = threading.Thread(target=run_async, args=(execute(command),))
    threded.start()
    return 'True'   

@app.route('/restartapp')
def restartapp():
    subprocess.run(f'python cleanup.py "' + config['command'] + f' ' + config['args'] + ' ' + config['executablepath'] + '"', shell=True)
    os.execv(sys.executable, [sys.executable] + sys.argv)
    subprocess.run(f'python cleanup.py "startup.py"', shell=True)

@app.route('/quit')
def quit():
    print("Quit")
    subprocess.run(f'python cleanup.py "' + config['command'] + f' ' + config['args'] + ' ' + config['executablepath'] + '"', shell=True)
    return "True"

@app.route('/quitapp')
def quitapp():
    subprocess.run(f'python cleanup.py "' + config['command'] + f' ' + config['args'] + ' ' + config['executablepath'] + '"', shell=True)
    os._exit(69)
    return "True"

@app.route('/f')
def j():
    return render_template('functions.js')

@app.route('/status')
def status():
    return jsonify({"message": "OK"}), 200

@app.route("/s")
def s():
    return render_template('status.js')


@app.route('/g')
def greg():
    return render_template('gremlin.js')

@app.route('/frame')
def frame():
    return render_template('frame.html')

@app.route('/w')
def webhookle():
    return render_template('webhooker.js')

def run():
    server.run_forever()



@app.route('/clone')
def clone():
     peter = urlparse(config['giturl'])
     path = peter.path
     reponame = os.path.basename(path)
     pathman = os.path.realpath(__file__)
     rereponame = str(reponame).replace('.git', '')
     print(f"{pathman}/{config['clonepath']}/{rereponame}")
     funnypaths = f"{pathman}/{config['clonepath']}/{rereponame}"
     funnypath = funnypaths.replace("/startup.py", "")
     print(funnypath)
     if os.path.exists(funnypath):
         print("I exist pal")
         subprocess.run(f'git -C {funnypath} pull', shell=True)
     else:
        subprocess.run(f'git clone https://{config["gituser"]}:{config["gitoken"]}@{config["giturl"]} {config["clonepath"]}', shell=True) # Modify this to your personal needs! Not everyone needs the authentication
     return "True"

if __name__ == "__main__":
    burger = threading.Thread(target=run)
    burger.start()
    app.run("0.0.0.0", use_reloader=False, port=config['port'])
