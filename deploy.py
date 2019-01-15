# It is implemented the Deploy, a command line interpreter tool that allows to deploy an arquitecture

import click

from subprocess import call
import logging
import sys
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pfinalp2')

@click.group()
def cli():
    pass

@cli.command()
def setupvnx():
    """Download the vnx xml of pfinal"""
    logger.debug("Download the vnx xml of pfinal")
    line = "wget http://idefix.dit.upm.es/cdps/pfinal/pfinal.tgz"
    call(line, shell=True)
    line = "sudo vnx --unpack pfinal.tgz"
    call(line, shell=True)
    line = "cd pfinal"
    call(line, shell=True)
    line = "bin/prepare-pfinal-vm"
    call(line, shell=True)

@cli.command()
def up():
    """Boot the system """
    logger.debug("Boot the system ")
    os.system("sudo vnx -f pfinal.xml --create")
    # os.system("sudo vnx -f pfinal.xml --show-map")

@cli.command()
def greetAll():
    """Create & show Hello.text in s1,s2,s3,lb,bbdd,nas1,nas2 & nas3"""

    for i in [1,2,3]:
      logger.debug('=> hello in ' + str(i))
      os.system("sudo lxc-attach --clear-env -n s"+ str(i) +" -- bash -c \"echo 'hello' > hello.txt \"" )
      os.system("sudo lxc-attach --clear-env -n s"+ str(i) +" -- bash -c ls")

    logger.debug('=> hello in lb')
    os.system("sudo lxc-attach --clear-env -n lb -- bash -c \"echo 'hello' > hello.txt \"")
    os.system("sudo lxc-attach --clear-env -n lb -- bash -c ls")

    logger.debug('=> hello in fw')
    os.system("sudo lxc-attach --clear-env -n fw -- bash -c \"echo 'hello' > hello.txt \"")
    os.system("sudo lxc-attach --clear-env -n fw -- bash -c ls")

    for i in [1,2,3]:
      logger.debug('=> hello in nas' + str(i))
      os.system("sudo lxc-attach --clear-env -n nas"+ str(i) +" -- bash -c \"echo 'hello' > hello.txt \"" )
      os.system("sudo lxc-attach --clear-env -n nas"+ str(i) +" -- bash -c ls")

    logger.debug('=> hello in bbdd')
    os.system("sudo lxc-attach --clear-env -n bbdd -- bash -c \"echo 'hello' > hello.txt \"")
    os.system("sudo lxc-attach --clear-env -n bbdd -- bash -c ls")

@cli.command()
def destroy():
    """Destroy the system"""
    click.echo("Destroy the system ")
    os.system("sudo vnx -f pfinal.xml --destroy")
    # os.system("sudo vnx -f pfinal.xml --show-map")

@cli.command()
def confbbdd():
    """Config the BBDD as in the statment"""

@cli.command()
def confcluster():
    """Config gluster in nasX and in front servers"""

@cli.command()
def conffront():
    """Config the front servers"""

@cli.command()
def greet():
    """Say hello in your machine"""
    click.echo("Hi")

@cli.command()
def bye():
    """Say bye in your machine"""
    click.echo("Bye")

@cli.command()
def test():
    """Test questions"""
    greet()
    question = raw_input("If no errors, may continue? (y/n)")
    while question.lower() not in ("y", "n"):
        click.echo(question[0])
        question = input("If there are no errors, may continue? (y/n)")
    if question != "y":
        bye()
    else:
       greet()

@cli.command()
@click.pass_context
def chain(ctx):
    """Test chain"""
    ctx.invoke(greet)
    ctx.invoke(bye)
