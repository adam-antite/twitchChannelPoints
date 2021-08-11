# Description

Kind of a hacky workaround to utilize the newest Twitch API based on WebSockets. Since Assetto Corsa apps only utilize Python 3.3.5 at the latest, this workaround launches a python 3.8 shell outside of the game to handle communication with the Twitch API and relaying this info to the in-game app.

## How to Install the AC App

Step 1) Open the zip file and drag the twitchChannelPoints folder into assettocorsa\apps\python

Step 2) Go to Content Manager Settings -> Assetto Corsa -> Apps -> make sure 'Twitch Channel Points' is checked and enabled.


## How to Set Up the Server Client:

Step 0) Make sure you have Python 3.8.6 installed and that you have added Python to your systems PATH variable.
	
	https://www.python.org/downloads/release/python-386/ 

	(download is at the bottom of the page; select the 'Windows x86-64 executable installer' 
	if you have 64-bit Windows or the 
	'Windows x86 executable installer' if you have 32-bit Windows.)

	1) Open the installer, click 'Customize Installation'.
	2) Click 'Next'
	3) Check the box next to 'Add python to environment variables'
	4) Click 'Install'
	

Step 1) Restart your computer if you had to install Python or make changes to your PATH variable in Step 0.

Step 2) Run the following command to verify your Python version is 3.8.x. If you get an error saying 'python is not recognized as an internal or external command...', then you need to add Python to your PATH variable. (see Step 0)

	python -V

Step 3) Run the following two commands to install the required Python modules for this app.

	pip install websockets
	pip install requests

Step 4) Copy and paste the following link into your browser. Login with twitch and authorize this app to allow it access to your Twitch chat. 


	https://id.twitch.tv/oauth2/authorize?client_id=e6egls0ukji6rok7lvw7kyhaf77woo&redirect_uri=http://localhost&response_type=token&scope=channel:read:redemptions%20user:read:email


Step 5) Once you have clicked Authorize, you will be redirected to a non-working address (see token_example.png). In the address bar, copy the part after access_token (red box in token_example.png) and paste it into the token section of WebSocketConfig.ini

Step 6) Enter your username in WebSocketConfig.ini