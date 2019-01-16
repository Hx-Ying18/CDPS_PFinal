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
@click.pass_context
def up(ctx):
    """Create and boot the system """
    logger.debug("[0/7] Boot the system ")
    os.system("sudo vnx -f pfinal.xml --create")
    # os.system("sudo vnx -f pfinal.xml --show-map")
    logger.debug("[1/7] System boot")
    question = raw_input("If no errors, may continue? (y/n)")
    while question.lower() not in ("y", "n"):
        # click.echo(question[0])
        question = input("If there are no errors, may continue? (y/n)")
    if question != "y":
        ctx.invoke(bye)
        ctx.invoke(destroy)
    else:
        ctx.invoke(fw)

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
@click.pass_context
def restart(ctx):
    """Destroy the system"""
    logger.info("Restart the system ")
    ctx.invoke(destroy)
    ctx.invoke(up)

@cli.command()
@click.pass_context
def bbdd(ctx):

    """Config the BBDD as in the statment"""

    logger.info("[2/7] Configuring BBDD  ")
    os.system('chmod 777 ../deployBBDD.sh')
    os.system('sudo cp ../deployBBDD.sh /var/lib/lxc/bbdd/rootfs/root')
    os.system('sudo lxc-attach --clear-env -n bbdd -- /root/deployBBDD.sh')

    # os.system('sudo cp ../testBBDD.sh /var/lib/lxc/bbdd/rootfs/root')
    # os.system('chmod 777 ../testBBDD.sh')
    # os.system('sudo lxc-attach --clear-env -n bbdd -- /root/testBBDD.sh')

    logger.info("[3/7] BBDD configured")

    question = raw_input("If no errors, may continue? (y/n)")
    while question.lower() not in ("y", "n"):
        # click.echo(question[0])
        question = input("If there are no errors, may continue? (y/n)")
    if question != "y":
        ctx.invoke(bye)
        ctx.invoke(destroy)
    else:
        ctx.invoke(cluster)

@cli.command()
@click.pass_context
def cluster(ctx):

    """Config gluster in nasX and in front servers"""

    logger.info("[3/7] Configuring storage cluster for images  ")
    os.system('chmod 777 ../configClusterInNas.sh')

    logger.info("[3/7] (0/4) Configuring the IPs in Nas ")
    for i in range(3):
        os.system('sudo cp ../configClusterInNas.sh /var/lib/lxc/nas'+str(i+1)+'/rootfs/root')

    for i in range(3):
        os.system('sudo lxc-attach --clear-env -n nas'+str(i+1)+' -- /root/configClusterInNas.sh')

    logger.info("[3/7] (1/4) setting the sync in the servers")
    os.system("sudo lxc-attach --clear-env -n nas1 -- gluster peer probe nas2")
    os.system("sudo lxc-attach --clear-env -n nas1 -- gluster peer probe nas3")
    os.system("sudo lxc-attach --clear-env -n nas1 -- gluster peer status")
    os.system("sudo lxc-attach --clear-env -n nas1 -- gluster volume create nas replica 3 nas1:/nas nas2:/nas nas3:/nas force")
    os.system("sudo lxc-attach --clear-env -n nas1 -- gluster volume start nas")

    logger.info("[3/7] (2/4) reducing the time to answer in the nas")
    for i in range(3):
        os.system('sudo lxc-attach --clear-env -n nas'+str(i+1)+' -- gluster volume set nas network.ping-timeout 5')

    os.system("sudo lxc-attach --clear-env -n nas1 -- gluster volume info")

    logger.info("[3/7] (3/4) mount the nas in servers")
    for i in range(3):
        os.system('sudo lxc-attach --clear-env -n s' + str(i + 1) + ' -- mkdir /mnt/nas')
        os.system('sudo lxc-attach --clear-env -n s' + str(i + 1) + ' -- mount -t glusterfs 20.2.4.21:/nas /mnt/nas')

    logger.info("[4/7] cluster configured")

    question = raw_input("If no errors, may continue? (y/n)")
    while question.lower() not in ("y", "n"):
        # click.echo(question[0])
        question = input("If there are no errors, may continue? (y/n)")
    if question != "y":
        ctx.invoke(bye)
        ctx.invoke(destroy)
    else:
        ctx.invoke(greet)

@cli.command()
@click.pass_context
def front():
    """Config the front servers"""



@cli.command()
def testCluster():
    """Cluster replicating?"""
    logger.info("(0/3) periodically creating in each server in /mnt/nas a file with the date")
    os.system("sudo lxc-attach --clear-env -n s1 -- bash -c \"echo 'hello' > /mnt/nas/3.txt \"")
    logger.debug("S1")
    os.system('sudo lxc-attach --clear-env -n s1 -- tree /mnt/nas')
    for i in range(3):
        logger.debug("nas"+str(i+1))
        os.system('sudo lxc-attach --clear-env -n nas'+ str(i+1) +' -- tree /nas')


@cli.command()
@click.pass_context
def fw(ctx):
    """FW only allows access through ping and to the port 80 of the lb"""
    logger.info("[1/7] Configuring firewall")
    # call('sudo lxc-attach --clear-env -n fw -- /root/fw.fw', shell=True)
    logger.info("[2/7] Configured firewall")
    question = raw_input("If no errors, may continue? (y/n)")
    while question.lower() not in ("y", "n"):
        # click.echo(question[0])
        question = input("If there are no errors, may continue? (y/n)")
    if question != "y":
        ctx.invoke(bye)
        ctx.invoke(destroy)
    else:
        ctx.invoke(greet)

@cli.command()
def greet():
    """Say hello in your machine"""
    click.echo("Hi")
    # for i in range(3):
    #     hi()
    # test()

def hi():
    click.echo("Hi!!!")

@cli.command()
def bye():
    """Say bye in your machine"""
    click.echo("Bye")

@cli.command()
@click.pass_context
def test1(ctx):
    """Test questions"""
    ctx.invoke(greet)
    question = raw_input("If no errors, may continue? (y/n)")
    while question.lower() not in ("y", "n"):
        click.echo(question[0])
        question = input("If there are no errors, may continue? (y/n)")
    if question != "y":
        ctx.invoke(bye)
    else:
        ctx.invoke(greet)

def test():
    """Test questions"""
    question = raw_input("If no errors, may continue? (y/n)")
    while question.lower() not in ("y", "n"):
        click.echo(question[0])
        question = input("If there are no errors, may continue? (y/n)")
    if question != "y":
        ctx.invoke(bye)
    else:
        ctx.invoke(greet)



@cli.command()
@click.pass_context
def chainTC(ctx):
    """Test chain"""
    ctx.invoke(greet)
    ctx.invoke(test1)

def chain(ctx):
    """Test chain"""
    ctx.invoke(greet)
    test()
