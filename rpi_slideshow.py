#!/usr/bin/python3
""" rpi_slideshow.py

Usage:
    rpi_slideshow.py <path> <delay>

"""

import docopt
import watchdog
import logging
import os
import time
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_feh_command_arglist(path, delay):
    return ["feh", path, "--fullscreen", "--auto-zoom", "--hide-pointer", "--slideshow-delay", str(delay)]

class SlideshowStarter(watchdog.events.FileSystemEventHandler):

    def __init__(self, delay):
        self.delay = delay

    def on_created(self, event):
        logger.info("Handling new directory %s", event.src_path)
        arglist = get_feh_command_arglist(event.src_path, self.delay)
        subprocess.call(arglist)
        logger.info("feh has quit")

if __name__ == "__main__":

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch.setFormatter(formatter)
    logger.addHandler(ch)

    args = docopt.docopt(__doc__)

    delay = float(args["<delay>"])
    path = os.path.realpath(args["<path>"])

    event_handler = SlideshowStarter(delay)

    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()

    logger.info("Starting rpi_slideshow")
    logger.info("Waiting for changes in %s", path)
    logger.info("Image change every %d seconds", delay)

    observer.join()