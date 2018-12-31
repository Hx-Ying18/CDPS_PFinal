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
    click.echo("Download the vnx xml of pfinal")
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
    click.echo("Boot the system ")
    os.system("sudo vnx -f pfinal.xml --create")
    # os.system("sudo vnx -f pfinal.xml --show-map")

@cli.command()
def greet():
    """Create a Hello.text in all machines and then show it."""
    click.echo('=> hello in s1')
    os.system("sudo lxc-attach --clear-env -n s1 -- bash -c \"echo 'hello' > hello.txt \"" )
    os.system("sudo lxc-attach --clear-env -n s1 -- bash -c ls")

@cli.command()
def destroy():
    """Destroy the system"""
    click.echo("Destroy the system ")
    os.system("sudo vnx -f pfinal.xml --destroy")
    # os.system("sudo vnx -f pfinal.xml --show-map")