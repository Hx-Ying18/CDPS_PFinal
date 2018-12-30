# It is implemented the Deploy, a command line interpreter tool that allows to deploy an arquitecture

from subprocess import call
import logging
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pfinalp2')

argsLen = len(sys.argv)
args = sys.argv

def setup():
    print('Hello world')
    # line = "wget http://idefix.dit.upm.es/cdps/pfinal/pfinal.tgz"
    # call(line, shell=True)
    # line = "sudo vnx --unpack pfinal.tgz"
    # call(line, shell=True)
    # line = "cd pfinal"
    # call(line, shell=True)
    # line = "bin/prepare-pfinal-vm"
    # call(line, shell=True)

if argsLen > 1:
    task = args[1]
    logger.debug("The task is : "+ str(task))

    if task == "setup":
        setup()
    elif task == "help":
        print()
else:
    print('This is not a Deploy command')






