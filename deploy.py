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
def start(ctx):
    """Create and boot the system """

    logger.debug("[0/7] Boot the system ")
    os.system("sudo vnx -f pfinal.xml --create")
    # os.system("sudo vnx -f pfinal.xml --show-map")
    # logger.debug("[1/7] System boot")
    # question = raw_input("If no errors, may continue? (y/n)")
    # while question.lower() not in ("y", "n"):
    #     # click.echo(question[0])
    #     question = input("If there are no errors, may continue? (y/n)")
    # if question != "y":
    #     ctx.invoke(bye)
    #     ctx.invoke(destroy)
    # else:
    #     ctx.invoke(greet)

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
def testbbdd(ctx):
    os.system('sudo cp ../testBBDD.sh /var/lib/lxc/bbdd/rootfs/root')
    os.system('chmod 777 ../testBBDD.sh')
    os.system('sudo lxc-attach --clear-env -n bbdd -- /root/testBBDD.sh')

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

    # question = raw_input("If no errors, may continue? (y/n)")
    # while question.lower() not in ("y", "n"):
    #     # click.echo(question[0])
    #     question = input("If there are no errors, may continue? (y/n)")
    # if question != "y":
    #     ctx.invoke(bye)
    #     ctx.invoke(destroy)
    # else:
    #     ctx.invoke(cluster)

@cli.command()
@click.pass_context
def cluster(ctx):

    """Config gluster in nasX and in front servers"""

    logger.info("[3/7] Configuring storage cluster for images  ")
    os.system('chmod 777 ../configClusterInNas.sh')

    logger.info("[3/7] (0/4) Configuring the IPs in Nas ")
    for i in range(3):
        os.system('sudo cp ../configClusterInNas.sh /var/lib/lxc/nas'+str(i+1)+'/rootfs/root')
        os.system('sudo lxc-attach --clear-env -n nas' + str(i + 1) + ' -- /root/configClusterInNas.sh')

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

    logger.info("[3/7] cluster configured?")

    # question = raw_input("If no errors, let's continue or test? (y/n/t)")
    # while question.lower() not in ("y", "n", "t"):
    #     # click.echo(question[0])
    #     question = input("If there are no errors, let's continue or test? (y/n/t)")
    # if question == "n":
    #     ctx.invoke(bye)
    #     ctx.invoke(destroy)
    # if question == "y":
    #     ctx.invoke(front)
    # else:
    #     # ctx.invoke(deletetc)
    #     # logger.debug("[3/7] Cluster test {0/5} starting")
    #     # ctx.invoke(tcluster)
    #     # logger.debug("[3/7] Cluster test {1/5} down nas 3")
    #     # ctx.invoke(downnas3)
    #     # logger.debug("[3/7] Cluster test {2/5} no in nas 3")
    #     # ctx.invoke(tcluster)
    #     # logger.debug("[3/7] Cluster test {3/5} check there is nothing in nas3 ")
    #     # ctx.invoke(upnas3)
    #     # ctx.invoke(shownas3)
    #     # logger.debug("[3/7] Cluster test {4/5} check there are files in nas 3 after up")
    #     # ctx.invoke(deletetc)
    #     # logger.debug("[4/7] Cluster test {5/5} ")
    #     # ctx.invoke(front)

@cli.command()
@click.pass_context
def maxtcluster(ctx):
    ctx.invoke(deletetc)
    logger.debug("[3/7] Cluster test {0/5} starting")
    ctx.invoke(tcluster)
    logger.debug("[3/7] Cluster test {1/5} down nas 3")
    ctx.invoke(downnas3)
    logger.debug("[3/7] Cluster test {2/5} no in nas 3")
    ctx.invoke(tcluster)
    logger.debug("[3/7] Cluster test {3/5} check there is nothing in nas3 ")
    ctx.invoke(upnas3)
    ctx.invoke(shownas3)
    logger.debug("[3/7] Cluster test {4/5} check there are files in nas 3 after up")
    ctx.invoke(deletetc)
    logger.debug("[4/7] Cluster test {5/5} ")

@cli.command()
@click.pass_context
def front(ctx):
    """Config the front servers"""
    logger.info("[4/7] (0/5) Configuring servers")
    logger.info("1. Install node and npm in the three servers ")
    logger.info("2. Clone the github repo")
    logger.info("3. Config it and check")
    logger.info("4. Make uploads in the nas ")
    logger.info("5. Check thru linx it can be get to the three servers")

    logger.info("(0/5) Install node and npm in the three servers ")
    ctx.invoke(installNpmNode)

    logger.info("(1/5) Clone the github repo")
    ctx.invoke(clone)

    logger.info("(2/5) Config and check")
    ctx.invoke(config)
    ctx.invoke(run)

    logger.info("(3/5). Make uploads in the nas ")
    #ctx.invoke(link)

    logger.info("(4/5). Do prerouting to the port 3000, from 80")
    # ctx.invoke(lynx) if doping this with yes | trigger stuck

    os.system(
        "sudo lxc-attach --clear-env -n s1 -- sudo iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to-port 3000")
    os.system(
        "sudo lxc-attach --clear-env -n s2 -- sudo iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to-port 3000")
    os.system(
        "sudo lxc-attach --clear-env -n s3 -- sudo iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to-port 3000")

    logger.info("(5/5). Done")
    # question = raw_input("If there are no errors, may continue? (y/n)")
    # while question.lower() not in ("y", "n"):
    #     # click.echo(question[0])
    #     question = raw_input("If there are no errors, may continue? (y/n)")
    # if question != "y":
    #     ctx.invoke(bye)
    #     ctx.invoke(destroy)
    # else:
    #    ctx.invoke(lb)



@cli.command()
def installNpmNode():
    """Install npm and nodejs"""
    for i in range(3):
        os.system('sudo lxc-attach --clear-env -n s'+str(i+1)+' -- sudo apt update')

        # Deprectaed, due to an error when migrating
        # os.system('sudo lxc-attach --clear-env -n s' + str(i + 1) + ' -- sudo apt -y install nodejs npm')

        os.system("curl -sL https://deb.nodesource.com/setup_9.x | sudo bash -")
        os.system("sudo apt-get install nodejs")

        os.system('sudo lxc-attach --clear-env -n s' + str(i + 1) + ' -- sudo apt -y install npm')

        os.system('sudo lxc-attach --clear-env -n s' + str(i + 1) + ' -- nodejs --version')
        os.system('sudo lxc-attach --clear-env -n s' + str(i + 1) + ' -- npm --version')

@cli.command()
def clone():
    """Clone"""
    for i in range(3):
        os.system('sudo lxc-attach --clear-env -n s' + str(i + 1) + ' -- git clone https://github.com/CORE-UPM/quiz_2019.git')
        os.system('sudo lxc-attach --clear-env -n s' + str(i + 1) + ' -- mv /quiz_2019 root/')

@cli.command()
def config():
    """Config"""

    for i in range(3):
        os.system('sudo cp ../deployServer.sh /var/lib/lxc/s'+str(i+1)+'/rootfs/root')
        os.system('sudo lxc-attach --clear-env -n s'+str(i+1)+' -- ./root/deployServer.sh')

# @cli.command()
# def migrate():
#     """Migrating"""
#
#     os.system('sudo cp ../migrateSeed.sh /var/lib/lxc/s1/rootfs/root')
#     os.system('sudo lxc-attach --clear-env -n s1 -- /root/migrateSeed.sh')

@cli.command()
def run():
    """Run service"""
    os.system("sudo lxc-attach --clear-env -n s1 -- pwd")
    os.system(
        "sudo lxc-attach --clear-env -n s1 -- bash -c \"cd /root/quiz_2019; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.2.4.31:3306/quiz; npm run-script migrate_cdps ; npm run-script seed_cdps; ./node_modules/forever/bin/forever start ./bin/www \"")
    os.system(
        "sudo lxc-attach --clear-env -n s2 -- bash -c \" cd /root/quiz_2019; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.2.4.31:3306/quiz; ./node_modules/forever/bin/forever start ./bin/www \"")
    os.system(
        "sudo lxc-attach --clear-env -n s3 -- bash -c \" cd /root/quiz_2019; export QUIZ_OPEN_REGISTER=yes; export DATABASE_URL=mysql://quiz:xxxx@20.2.4.31:3306/quiz; ./node_modules/forever/bin/forever start ./bin/www \"")


@cli.command()
def link():
    """Link upload with nas"""
    os.system('sudo cp ../link.sh /var/lib/lxc/s1/rootfs/root')
    os.system('sudo lxc-attach --clear-env -n s1 -- ./root/link.sh')
    for k in range(3):
        os.system('sudo cp ../link.sh /var/lib/lxc/s'+str(k+1)+'/rootfs/root')
        os.system('sudo lxc-attach --clear-env -n s'+str(k+1)+' -- ./root/link.sh')


@cli.command()
@click.pass_context
def tlink(ctx):
    """Cluster replicating?"""
    logger.info("=> Testing replication of cluster: each server a file in /root/quiz_2019/public/uploads ")

    logger.debug("[3/7] (0/3) No files in nas")
    for k in range(3):
         os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- tree /root/quiz_2019/public/uploads/nas ")

    for k in range(3):
        logger.debug("(0/3) "+str(k+1)+"/3 No files in nas"+ str(k+1))
        # os.system('sudo lxc-attach --clear-env -n s' + str(k + 1) + ' -- chmod 777 /mnt/nas/*')
        os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- tree /root/quiz_2019/public/uploads ")
        os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- ls -l /root/quiz_2019/public/uploads ")
        # os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- rm /mnt/nas/*")

    logger.debug("(1/3) Creating files")

    for k in range(3):
        os.system("sudo lxc-attach --clear-env -n s"+ str(k+1)+ " -- bash -c \"echo 'hello' > /root/quiz_2019/public/uploads/nas/S"+str(k+1))
            # os.system('sudo lxc-attach --clear-env -n s' + str(k + 1) + ' -- chmod 777 /mnt/nas/*')

    logger.debug("(2/3) Show the files")
    for k in range(3):
        logger.debug("S" + str(k+1))
        os.system('sudo lxc-attach --clear-env -n s' + str(k + 1) + ' -- tree /root/quiz_2019/public/uploads/nas')
    for i in range(3):
        logger.debug("nas" + str(i + 1))
        os.system('sudo lxc-attach --clear-env -n nas' + str(i + 1) + ' -- tree /nas')

    #for k in range(3):
    # os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- ls -l /mnt/nas")
    #     os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- cd /mnt/nas")
    #     os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- ls")
    #     os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- rm /mnt/nas/*")

    question = raw_input("Check the replication. If no errors, may continue? (y/n)")
    while question.lower() not in ("y", "n"):
        # click.echo(question[0])
        question = input("Check the replication. If there are no errors, may continue? (y/n)")
    if question != "y":
        ctx.invoke(bye)
        ctx.invoke(destroy)
    else:
        logger.debug("(3/3) Test done")


@cli.command()
def lynx():
    """Lynx"""
    for i in range(3):
        os.system('sudo lxc-attach --clear-env -n s' + str(i + 1) + ' -- lynx -term=vt100 http://20.2.3.11:3000')

@cli.command()
@click.pass_context
def lb(ctx):
    """Installs haproxy"""
    logger.info("[5/7] Haproxy")
    os.system('sudo lxc-attach --clear-env -n lb -- sudo apt update')
    os.system('sudo lxc-attach --clear-env -n lb -- sudo apt install -y haproxy')
    os.system('sudo lxc-attach --clear-env -n lb -- haproxy -v')

    logger.info("Move the haproxy.cfg into the lb")
    os.system('sudo cp ../haproxy.cfg /var/lib/lxc/lb/rootfs/root')
    os.system('sudo lxc-attach --clear-env -n lb -- mv /root/haproxy.cfg /etc/haproxy/haproxy.cfg')

    logger.info("Restart haproxy")
    os.system('sudo lxc-attach --clear-env -n lb -- sudo service haproxy restart')


    # question = raw_input("Check the replication. If no errors, may continue? (y/n)")
    # while question.lower() not in ("y", "n"):
    #     # click.echo(question[0])
    #     question = input("Check the replication. If there are no errors, may continue? (y/n)")
    # if question != "y":
    #     ctx.invoke(bye)
    #     ctx.invoke(destroy)
    # else:
    #    ctx.invoke(fw)


@cli.command()
@click.pass_context
def tlb(ctx):
    """Installs haproxy"""
    logger.info("Test Haproxy")
    os.system("sudo lxc-attach --clear-env -n fw -- while true; do curl 20.2.2.2;sleep 0.1; done; ")

@cli.command()
@click.pass_context
def tcluster(ctx):
    """Cluster replicating?"""
    logger.info("=> Testing replication of cluster: each server a file in /mnt/nas ")

    logger.debug("[3/7] (0/3) No files in nas")
    for k in range(3):
         os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- rm -r -- /mnt/nas/testCluster")

    for k in range(3):
        logger.debug("(0/3) "+str(k+1)+"/3 No files in nas"+ str(k+1))
        # os.system('sudo lxc-attach --clear-env -n s' + str(k + 1) + ' -- chmod 777 /mnt/nas/*')
        os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- tree /mnt/nas")
        os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- ls -l /mnt/nas")
        # os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- rm /mnt/nas/*")

    logger.debug("(1/3) Creating files")

    os.system('sudo lxc-attach --clear-env -n s1 -- mkdir /mnt/nas/testCluster')

    for k in range(3):
        for j in range(1):
            os.system("sudo lxc-attach --clear-env -n s"+ str(k+1)+ " -- bash -c \"echo 'hello' > /mnt/nas/testCluster/S"+str(k+1)+"_"+ str(j) +" \"")
            # os.system('sudo lxc-attach --clear-env -n s' + str(k + 1) + ' -- chmod 777 /mnt/nas/*')

    logger.debug("(2/3) Show the files")
    for k in range(3):
        logger.debug("S" + str(k+1))
        os.system('sudo lxc-attach --clear-env -n s' + str(k + 1) + ' -- tree /mnt/nas/testCluster')
    for i in range(3):
        logger.debug("nas" + str(i + 1))
        os.system('sudo lxc-attach --clear-env -n nas' + str(i + 1) + ' -- tree /nas/testCluster')

    #for k in range(3):
    # os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- ls -l /mnt/nas")
    #     os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- cd /mnt/nas")
    #     os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- ls")
    #     os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- rm /mnt/nas/*")

    logger.debug("It should not be any files in nas, and files in the nas if it's the fisrt command run")
    logger.debug("And no files in the nas3 if it is the second run")
    # question = raw_input("Check the replication. If no errors, may continue? (y/n)")
    #
    # while question.lower() not in ("y", "n"):
    #     # click.echo(question[0])
    #     question = input("Check the replication. If there are no errors, may continue? (y/n)")
    # if question != "y":
    #     ctx.invoke(bye)
    #     ctx.invoke(deletetc)
    #     ctx.invoke(destroy)
    # else:
    #     logger.debug("(3/3) Test done")


@cli.command()
def downnas3():
    """Cluster replicating?"""
    os.system('sudo lxc-attach --clear-env -n nas3 -- ifconfig eth1 down')

@cli.command()
def upnas3():
    """Cluster replicating?"""
    os.system('sudo lxc-attach --clear-env -n nas3 -- ifconfig eth1 up')

@cli.command()
@click.pass_context
def fw(ctx):
    """FW only allows access through ping and to the port 80 of the lb"""
    logger.info("[1/7] Configuring firewall")
    # os.system('sudo cp ../fw.fw /var/lib/lxc/fw/rootfs/root')
    # os.system('sudo lxc-attach --clear-env -n fw -- chmod 777 /root/fw.fw')
    # os.system('sudo lxc-attach --clear-env -n fw -- sh /root/fw.fw')

    cmd_line = "sudo cp ../fw.fw /var/lib/lxc/fw/rootfs/root"
    call(cmd_line, shell=True)

    logger.info("[2/7] Configured firewall")

    cmd_line = "sudo lxc-attach --clear-env -n c1 -- nmap -F 20.2.2.2"
    call(cmd_line, shell=True)

    cmd_line = "sudo lxc-attach --clear-env -n fw -- chmod 777 /root/fw.fw"
    call(cmd_line, shell=True)

    cmd_line = "sudo lxc-attach --clear-env -n fw -- /root/fw.fw"
    call(cmd_line, shell=True)

    cmd_line = "sudo lxc-attach --clear-env -n c1 -- nmap -F 20.2.2.2"
    call(cmd_line, shell=True)

    # question = raw_input("If no errors, may continue? (y/n)")
    # while question.lower() not in ("y", "n"):
    #     # click.echo(question[0])
    #     question = input("If there are no errors, may continue? (y/n)")
    # if question != "y":
    #     ctx.invoke(bye)
    #     ctx.invoke(destroy)
    # else:
    #     logger.info("Configured")

@cli.command()
@click.pass_context
def tfw(ctx):
    """FW only allows access through ping and to the port 80 of the lb"""
    logger.info("Testing firewall")
    os.system('sudo lxc-attach --clear-env -n c1 -- nmap -F 20.2.1.1')
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
def greet(ctx):
    """Say hello in your machine"""
    i = 0
    click.echo("Hi")
    ctx.invoke(bye)
    ctx.invoke(hi)
    i += 1
    click.echo(i)

    # for i in range(3):
    #     hi()
    # test()

@cli.command()
def hi():
    click.echo("Hi!!!")

@cli.command()
def bye():
    """Say bye in your machine"""
    click.echo("Bye")

@cli.command()
def shownas3():
    """Show nas 3"""
    logger.debug("Check after up there are files in nas3")
    os.system('sudo lxc-attach --clear-env -n nas3 -- tree /nas/testCluster')
    question = raw_input("If no errors, may continue? (y/n)")
    while question.lower() not in ("y", "n"):
        # click.echo(question[0])
        question = input("If there are no errors, may continue? (y/n)")
    if question != "y":
        ctx.invoke(bye)
        ctx.invoke(deletetc)
        ctx.invoke(destroy)
    else:
        logger.debug("=> Cluster test done")

@cli.command()
def deletetc():
    """Delete test cluster"""
    os.system('sudo lxc-attach --clear-env -n nas3 -- tree /nas/testCluster')
    for k in range(3):
         os.system("sudo lxc-attach --clear-env -n s" + str(k + 1) + " -- rm -r -- /mnt/nas/testCluster")
    os.system('sudo lxc-attach --clear-env -n nas3 -- tree /nas/testCluster')

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

@cli.command()
@click.pass_context
def up(ctx):
    """Deployment up"""
    i = 0
    logger.debug("=>{"+str(i)+"/7} Start the deployment")
    ctx.invoke(start)
    ctx.invoke(ask)
    i += 1

    logger.debug("=>{"+str(i)+"/7} Config the BBDD")
    ctx.invoke(bbdd)
    ctx.invoke(ask)
    i += 1



@cli.command()
@click.pass_context
def go(ctx):
    """Deployment, after bbdd check"""

    i = 2
    logger.debug("=>{"+str(i)+"/7} Config the cluster")
    ctx.invoke(cluster)
    ctx.invoke(ask)
    i += 1

    logger.debug("=>{" + str(i) + "/7} Test the cluster")
    ctx.invoke(maxtcluster)
    ctx.invoke(ask)
    i += 1

    logger.debug("=>{" + str(i) + "/7} Config servers")
    ctx.invoke(front)
    ctx.invoke(ask)
    i += 1

    logger.debug("=>{" + str(i) + "/7} Config lb")
    ctx.invoke(lb)
    ctx.invoke(ask)
    i += 1

    logger.debug("=>{" + str(i) + "/7} Config lb")
    ctx.invoke(fw)
    ctx.invoke(ask)
    i += 1

    logger.debug("=>{" + str(i) + "/7} Up")

@cli.command()
@click.pass_context
def ask(ctx):
    """Ask to continue"""
    question = raw_input("If no errors, may continue? (y/n)")
    while question.lower() not in ("y", "n"):
        click.echo(question[0])
        question = input("If there are no errors, may continue? (y/n)")
    if question == "n":
        ctx.invoke(bye)
        ctx.invoke(destroy)
    if question == "t":
        logger.debug("Let's test")
    else:
        logger.debug("Let's continue")

@cli.command()
@click.pass_context
def ask(ctx):
    """Ask to continue"""
    question = raw_input("If no errors, may continue? (y/n)")
    while question.lower() not in ("y", "n"):
        click.echo(question[0])
        question = input("If there are no errors, may continue? (y/n)")
    if question == "n":
        ctx.invoke(bye)
        ctx.invoke(destroy)
    if question == "t":
        logger.debug("Let's test")
    else:
        logger.debug("Let's continue")

@cli.command()
@click.pass_context
def testask(ctx):
    """Ask to continue"""
    question = raw_input("If no errors, may continue? (y/n)")
    while question.lower() not in ("y", "n"):
        click.echo(question[0])
        question = input("If there are no errors, may continue? (y/n)")
    if question == "n":
        ctx.invoke(bye)
    if question == "t":
        logger.debug("Let's test")
    else:
        logger.debug("Let's continue")

@cli.command()
@click.pass_context
def testask2(ctx):
    """Ask to continue"""
    ctx.invoke(testask)
    ctx.invoke(bye)