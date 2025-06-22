# Configuration
Most config settings are in the `config.json` file, but you will need to edit the websocket URL in the `webhooker.js` file to match your local ip address or if you have a local domain you can set it to that.
You will probably also need to edit some info on the `startup.py` file to match your local setup.
(This is intended for Debian distros of Linux, but it should work on other distros with some minor modifications)
### Installation
1. Once you've obtained the code, run `python -m venv venv` to create a virtual environment which is required for this to run properly.
2. Run `source venv/bin/activate` to activate the virtual environment.
3. Run `pip install -r requirements.txt` to install all the required packages.
4. Run `python startup.py` to start the site with the settings you've configured.
5. If nessisary, modify the script to your personal needs.
