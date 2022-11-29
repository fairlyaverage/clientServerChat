import re, random
DELIMITER = ':' # formatting

def active_clients_to_string(active_clients):
    o = ""
    for key in active_clients:
        o += key + ','
    return o[:-1] # return string without last ',' character, at position -1

def active_client_ids_from_string(active_clients_string):
    active_client_ids = re.split(',', active_clients_string)
    return active_client_ids

def deformat_message(data): # process_data()?
    # expects encoded string of the format "to_client_id:from_client_id:flag:message"
    to_client_id, from_client_id, flag, message = re.split(DELIMITER, data.decode(), 3)
    return to_client_id, from_client_id, flag, message

def format_message(to_client_id, from_client_id, flag, message): # encode_and_format_client_message()?
    # params should be all strings, returns b"client_id:flag:message"
    """
            concatenate to_client_id + ':' + from_client_id + ':' + flag + ':' + message
            encode()
    """
    temp = ""
    temp += to_client_id + DELIMITER + from_client_id + DELIMITER + flag + DELIMITER + message
    return temp.encode()
