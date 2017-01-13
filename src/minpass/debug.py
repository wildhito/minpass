# Change value to enable / disable debug messages
PRINT_DEBUG_MESSAGES = False


def debug(msg):
    if PRINT_DEBUG_MESSAGES:
        print("> " + msg)
