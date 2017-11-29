#!/usr/bin/python
import logging

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create file handler which and set level to debug
fh = logging.FileHandler('pythonLogging.log')
fh.setLevel(logging.WARNING)
# create formatter
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add ch and fh to logger
logger.addHandler(ch)
logger.addHandler(fh)

# "application" code
logger.debug("debug message")
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.critical("critical message")

print('\nDone')
