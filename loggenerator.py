#!/usr/bin/python2.7
import time
import datetime
import logging
from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler


# Example "./loggenerator.py -l 40000 -s 60", will generate a 109MB of logfiles in one minute

parser = ArgumentParser()

parser.add_argument("-l", "--lps", dest="lps",
                    help="logs lines to be written per second", metavar="Logs per second", type=int, required=True)

parser.add_argument("-s", "--seconds", dest="seconds",
                    help="number of seconds to write logs for", metavar="seconds", type=int, required=True)

args = parser.parse_args()

print("Writing %s loglines per second for %s seconds to file loladtest.log" % (args.lps, args.seconds))

logger = logging.getLogger("loadtest_logger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("loadtest.log", maxBytes=1000000000, backupCount=4)  # 1GB MaxBytes, 5 files max, i.e. live file + 4 backup (5GB generated MAX)
logger.addHandler(handler)

for i in range(0, args.seconds):
    for j in range(0, args.lps):
        line = "[%s] Second %s LogLineNo %s" % (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), i, j)
        logger.info(line)
    time.sleep(1)
