import socket, threading, ssl
from shared_functions import *

NUMBER_OF_CONNECTIONS = 25
active_clients = dict()
active_client_threads = dict()
host = socket.gethostname()
port = 12342

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/path/to/certchain.pem', '/path/to/private.key')

def unique_client_id(client_id):
    if client_id in active_clients.keys():
        return False
    return True

def server_broadcast(message, flag): # special use for server broadcast-to-all
    for client in active_clients:
        """ updated active_clients broadcast, use flag = 6 """
        outgoing = format_message(client, "server", flag, message) # to, from, flag, message
        active_clients[client][0].send(outgoing)

        # debug only:
        print("server broadcast to all clients: ", message)

def listen_to_client(client_socket):
    global active_clients, active_client_threads, from_client_id
    while True: # to-do, while this client is connected/socket exists in list of active_clients/etc.
        """ listen for message """
        data = client_socket.recv(1024) # standby until a message is received
        to_client_id, from_client_id, flag, message = deformat_message(data) # determine what to do based on flag

        """ process message based on flag """
        if (flag == "1"): # client-to-client message
            # must ensure destination client exists, currently assume it does
            active_clients[to_client_id][0].send(data) # data is still formatted, encoded

            # debug only:
            print("server forwarded: {0} to {1} from {2}".format(message, to_client_id, from_client_id))
        elif (flag == "2"): # client-to-many
            pass
        elif (flag == "3"): # server-notification/error, send to all
            for client in active_clients:
                active_clients[client][0].send(data)
            pass
        elif (flag == "4"): # client-to-server new_client_id
            pass
        elif (flag == "5"):
            # debug only
            print("{0} disconnected from the server".format(from_client_id))

            active_clients[from_client_id][0].close() # close connection
            del active_clients[from_client_id] # delete
            # update_active_clients()
            server_broadcast(active_clients_to_string(active_clients), "6") # 6 == update to active clients
            break # quit loop, stop listening thread
        else:
            print("flag not recognized")
            pass

def new_client_connection():
    global server_socket, active_clients, active_client_threads
    new_client_connection = server_socket.accept()

    data = new_client_connection[0].recv(1024)
    new_client_id = data.decode()

    """ server checks client_id for uniqueness """
    if unique_client_id(new_client_id): # if user provided a unique id
        active_clients[new_client_id] = new_client_connection
    else: # server concatenates a random integer to user's provided id a unique identifier is confirmed
        try_client_id = new_client_id # initialize for scope
        while not unique_client_id(try_client_id):
            # try_client_id = new_client_id
            random_value = str(random.randint(0, 1023))
            try_client_id = new_client_id + random_value
        new_client_id = try_client_id
        active_clients[new_client_id] = new_client_connection

    """ server responds to client, first message confirms client's id """
    new_client_connection[0].send(new_client_id.encode())

    """ spawn thread and begin listening """
    t = threading.Thread(target=listen_to_client, args=(new_client_connection[0],), daemon=True)
    t.start()
    active_client_threads[new_client_id] = t # no real need to save this
    # upon connection init, broadcast [updated] active_client_ids
    server_broadcast(active_clients_to_string(active_clients), "6")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as u_server_socket:
    u_server_socket.bind((host, port))
    u_server_socket.listen(NUMBER_OF_CONNECTIONS)
    with context.wrap_socket(u_server_socket, server_side=True) as server_socket:

        # debug only
        print("Listening for connections...")

        while True: # always listening for new clients
            new_client_connection() # establish new connection; note that this is broken


# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = socket.gethostname()
# port = 12342

# server_socket.bind((host, port))
# server_socket.listen(NUMBER_OF_CONNECTIONS)

