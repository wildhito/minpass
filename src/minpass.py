#!/usr/bin/env python3
import argparse
from minpass.console import Console
from minpass.debug import PRINT_DEBUG_MESSAGES
from minpass.ui import UI


def main():
    parser = argparse.ArgumentParser(description="""
minpass is a minimalistic cross-platform password manager
for advanced configuration, copy config.json.dist into your own config.json
""", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('keyring_path', nargs='?', help='a keyring filepath')
    args = parser.parse_args()

    if not args.keyring_path:
        parser.print_help()
        return 1

    console = Console()
    if not console.load_keyring(args.keyring_path):
        return 2

    return console.run()


if __name__ == "__main__":
    if PRINT_DEBUG_MESSAGES:
        if not UI.confirm("Warning: debug messages are ON. Continue?", True):
            exit(0)

    exit_code = main()

    print("Reminder: if passwords were printed on screen, " \
          "remember to reset your console output (linux: clear, windows: cls)")
    exit(exit_code)
