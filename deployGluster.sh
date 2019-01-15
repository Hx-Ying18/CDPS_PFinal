#!/usr/bin/env bash

gluster peer probe 10.1.4.22
gluster peer probe 10.1.4.23

gluster volume create nas replica 3 10.1.4.21:/nas 10.1.4.22:/nas 10.1.4.23:/nas force
gluster volume start nas
gluster volume set nas network.ping-timeout 5