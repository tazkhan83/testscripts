#!/usr/bin/python2.7
import time
import datetime
import logging
from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler
from threading import Thread
from string import ascii_uppercase

# Example "./log_generator_multithreaded.py -l 1000 -s 60", will generate a 10 logfiles of 3 MB each (30MB total)
# Node: Time taken is dependent on processing power


def createRotatingLog(filename):
    print("Creating Logger For %s" % (filename))
    logger = logging.getLogger(filename)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(filename, maxBytes=1000000000, backupCount=1)  # 1GB MaxBytes, 2 files max, i.e. live file + 1 backup (2GB generated MAX per handler)
    logger.addHandler(handler)
    return logger


def writeToRotatingLog(logger):
    for i in range(0, args.seconds):
        for j in range(0, args.lps):
            line = "[%s] Second %s LogLineNo %s" % (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), i, j)
            logger.info(line)
        time.sleep(1)


if __name__ == "__main__":
    start = time.time()

    parser = ArgumentParser()

    parser.add_argument("-l", "--lps", dest="lps",
                        help="logs lines to be written per second", metavar="Logs per second", type=int, required=True)

    parser.add_argument("-s", "--seconds", dest="seconds",
                        help="number of seconds to write logs for", metavar="seconds", type=int, required=True)

    args = parser.parse_args()

    print("Writing %s loglines per second for %s seconds to 10 files loladtestA.log->loadtestJ.log" % (args.lps, args.seconds))

    fileList = []

    for c in ascii_uppercase:
        # create filnames from with extensions A-J
        if c == "K":
            break
        filename = "loadtest%s_%s.log" % (c, int(time.time()))
        fileList.append(filename)

    threadsList = []

    for i in range(len(fileList)):
        logger = createRotatingLog(fileList[i])
        thread = Thread(target=writeToRotatingLog, args=(logger, ))
        threadsList.append(thread)
        thread.start()

    for j in range(len(threadsList)):
        threadsList[j].join()

    print("Completed Writing Logfiles in %s seconds" % (time.time() - start))
