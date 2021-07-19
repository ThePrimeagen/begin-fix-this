import argparse
import signal
import sys
import melee
from typing import List, Dict
from dataclasses import dataclass
import traceback

from game_loop import Game, run_game_loop

# Assumed there is a p1 and p2 specified

@dataclass
class Args:
    port: int
    opponent: int
    debug: bool
    address: str
    dolphin_executable_path: str
    connect_code: str
    iso: str

# This example program demonstrates how to use the Melee API to run a console,
#   setup controllers, and send button presses over to a console

def check_port(value) -> int:
    ivalue = int(value)
    if ivalue < 1 or ivalue > 4:
        raise argparse.ArgumentTypeError("%s is an invalid controller port. \
                                         Must be 1, 2, 3, or 4." % value)
    return ivalue

def parse_args() -> Args:
    parser = argparse.ArgumentParser(description='Example of libmelee in action')
    parser.add_argument('--port', '-p', type=check_port,
            help='The controller port (1-4) your AI will play on',
            default=2)
    parser.add_argument('--opponent', '-o', type=check_port,
            help='The controller port (1-4) the opponent will play on',
            default=1)
    parser.add_argument('--debug', '-d', action='store_true',
            help='Debug mode. Creates a CSV of all game states')
    parser.add_argument('--address', '-a', default="127.0.0.1",
            help='IP address of Slippi/Wii')
    parser.add_argument('--dolphin_executable_path', '-e', default=None,
            help='The directory where dolphin is')
    parser.add_argument('--connect_code', '-t', default="",
            help='Direct connect code to connect to in Slippi Online')
    parser.add_argument('--iso', type=str,
            required=True, help='Path to melee iso.')

    return parser.parse_args()

if __name__ == "__main__":

    args = parse_args()

    log = None
    if args.debug:
        log = melee.Logger()

    console = melee.Console(path=args.dolphin_executable_path,
                            slippi_address=args.address,
                            logger=log)
    console.run(iso_path=args.iso)
    p2c = melee.Controller(console=console,
            port=args.port,
            type=melee.ControllerType.STANDARD)
    p1c = melee.Controller(console=console,
            port=args.opponent,
            type=melee.ControllerType.STANDARD)

    print("Connecting to console...")
    if not console.connect():
        print("ERROR: Failed to connect to the console.")
        sys.exit(-1)
    print("Console connected")
    print("Connecting controller to console...")
    if not p1.connect() or not p2.connect():
        print("ERROR: Failed to connect the controller.")
        sys.exit(-1)
    print("Controllers connected")

    game = Game(console, p1, p2, log=log)
    run_game_loop(game)

    # This isn't necessary, but makes it so that Dolphin will get killed when you ^C
    def signal_handler(sig, frame):
        console.stop()
        if args.debug:
            log.writelog()
            print("") #because the ^C will be on the terminal
            print("Log file created: " + log.filename)
        print("Shutting down cleanly...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
