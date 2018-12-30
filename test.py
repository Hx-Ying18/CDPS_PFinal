from subprocess import call
import logging
import sys

def firstsetup():
    print('Hello world')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pfinalp2')

argsLen = len(sys.argv)
args = sys.argv

if len > 1:
    task = args[1]
    logger.debug("The task is :"+ str(task))

    if task == "firstSetup":
        firstsetup()
else:
    print('This is not a deploy command')



