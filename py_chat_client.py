import socket, threading
from shared_functions import *

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12342

last_from_client_id = None # will hold last received client id for messages with "" to_user_id

active_client_ids = []
client_id = input("Enter a Client ID; Press [enter] to connect to server: ")
ss.connect((host, port))
# initial message always resolves client_id
ss.send(client_id.encode())
# # debug only:
# print("tried to send ", client_id)
data = ss.recv(1024)
client_id = data.decode()

# debug only:
print("<server>: Unique Client ID is ", client_id)

def get_messages_from_server():
    while True:
        data = ss.recv(1024)
        _, from_client_id, flag, message = deformat_message(data)

        if (flag == "6"):
            global active_client_ids
            active_client_ids = active_client_ids_from_string(message)
            print("<server>: Active Client IDs: {0}".format(active_client_ids))
        else:
            print("<{2}>: {0} is encoded as {1}".format(data, type(data), from_client_id)) # used to show data is encoded as a bytestream
            print("<{0}>: {1}".format(from_client_id, message))

            # save from_client_id for responding without specifying client_id
            global last_from_client_id
            last_from_client_id = from_client_id

t = threading.Thread(target=get_messages_from_server, daemon=True)
t.start()

while True:
    send_to_client_id = input("Recipient? Enter a client id: \n") # [Enter] to respond or Enter a client id to message a specific user
    message = input("<To {0}>: ".format(send_to_client_id if (send_to_client_id != "") else last_from_client_id)) # format using: specified client id otherwise respond to client id who sent the last message

    if (message == ".exit"):
        flag = "5" # "5" used to disconnect from server
        outgoing = format_message("server", client_id, flag, "")
        ss.send(outgoing) # alert server to disconnection
        ss.close() # close socket
        break # immediately break out of loop after disconnecting

    if (send_to_client_id == ""):
        # respond to last_from_client_id
        outgoing = format_message(last_from_client_id, client_id, "1", message) # only difference is substitution of last known client id if left blank
        ss.send(outgoing)
    else:
        # specify send_to_client_id
        flag = "1"
        outgoing = format_message(send_to_client_id, client_id, flag, message)
        ss.send(outgoing)

# debug only
print("Disconnected from server")

exit() # close client
