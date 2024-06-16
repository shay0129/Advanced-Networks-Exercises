PORT = 25   # Standard SMTP port for sending emails

# Server responses
SMTP_SERVICE_READY = "220" # SMTP service ready
REQUESTED_ACTION_COMPLETED = "250"  # Generic success response
COMMAND_SYNTAX_ERROR = "500" # Syntax error, command unrecognized
INCORRECT_AUTH = "535" # Authentication failedת Invalid credentials
ENTER_MESSAGE = "354"

# Authentication negotiation
AUTH_INPUT = "334" # Username:
AUTH_SUCCESS = "235" # Authentication successful

# Ending message
EMAIL_END = "\r\n.\r\n"  # Combination of chars to indicate email content ends
GOODBYE = "221" # closing connectionת Server goodbye message
