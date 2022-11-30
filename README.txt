Requirements:
	Python3.x+, which can be found at https://www.python.org/downloads/ along with installation instructions

Installation Instructions:	
	1.	Extract contents of SchwarzmanElliott_clientServerChat.zip
	2.	Open a terminal window and run the server script:
			on Linux/Unix systems: python3 py_chat_server.py
			on Windows: py py_chat_server.py
	3.	Run any number of client scripts in separate terminal instances:
			on Linux/Unix: python3 py_chat_client.py
			on Windows: py py_chat_client.py

FILES:
	py_chat_server.py
	py_chat_client.py
	shared_functions.py
	saved_values.cfg
	
Operating instructions:
	Server:
		There is no user interaction with the server, but actions can be monitored in the terminal interface.
		
	Client: 
		Connecting: After the initial prompt, type into the terminal a proposed client ID such as: Myusername, then press the [Enter] or [Return] key. The server will confirm your client ID - if it is unique it should match your proposed ID, but if another active client is already using the proposed ID then the server will append a random integer value to your proposed ID. Now you are connected to the server, and any messages you receive will be displayed in your interface.
		
		Messaging: Once connected, you may message any connected client. Each message requires two keyboard inputs each followed by [Enter] or [Return]: (1) the client ID for a user you wish to message and (2) the message you wish to send. After sending a message, your interface returns to (1) and awaits further input.
			1 a) client ID may be specified from among the list of Active Client IDs which is displayed periodically (whenever a user connects or disconnects) in your terminal. Simply enter a name contained in the list excluding the single quotation marks.
			1 b) alternatively, you may omit a client ID after receiving a message in order to respond to the last user that sent a message to you. Simply press [Enter] or [Return] without entering a client's ID.
			2 a) enter a plaintext message, and the server will forward it to the client specified in the previous step
			2 b) alternatively, if you wish to disconnect enter the command ".exit" omiting quotation marks.
