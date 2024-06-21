# Protocol Constants
CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT"
}  # .. Add more commands if needed

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR"
}  # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occurred
    """
    if not isinstance(cmd, str) or not isinstance(data, str):
        return ERROR_RETURN

    cmd = cmd.strip().ljust(CMD_FIELD_LENGTH)
    if len(cmd) > CMD_FIELD_LENGTH:
        return ERROR_RETURN

    data_len = len(data)
    if data_len > MAX_DATA_LENGTH:
        return ERROR_RETURN

    data_len_str = f"{data_len:0{LENGTH_FIELD_LENGTH}}"
    if len(data_len_str) > LENGTH_FIELD_LENGTH:
        return ERROR_RETURN

    full_msg = f"{cmd}{DELIMITER}{data_len_str}{DELIMITER}{data}"
    return full_msg


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occurred, returns None, None
    """
    if not isinstance(data, str):
        return ERROR_RETURN, ERROR_RETURN

    parts = data.split(DELIMITER)
    if len(parts) != 3:
        return ERROR_RETURN, ERROR_RETURN

    cmd, length_str, msg = parts
    cmd = cmd.strip()

    length_str = length_str.strip()
    if not length_str.isdigit() or len(length_str) > LENGTH_FIELD_LENGTH:
        return ERROR_RETURN, ERROR_RETURN

    msg_len = int(length_str)
    if msg_len != len(msg):
        return ERROR_RETURN, ERROR_RETURN

    return cmd, msg


def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occurred, returns None
    """
    parts = msg.split(DATA_DELIMITER)
    if len(parts) != expected_fields + 1:
        return [ERROR_RETURN]

    return parts


def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of its fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    if not all(isinstance(field, (str, int, float)) for field in msg_fields):
        return ERROR_RETURN

    return DATA_DELIMITER.join(str(field) for field in msg_fields)
