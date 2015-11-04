#!/usr/bin/python
import re

nodes = {}
routers = {}

def parse_topology(file):
    lines = file.split('\n')
    cat = ''
    for line in lines:
        if line[0] == '#':
            cat = line[1:len(line)]
            continue
        values = line.split(',')
        if cat == 'NODE':
            ip=values[2].split('/')
            create_node(name=values[0], mac=values[1], ip=ip[0], mask=ip[1], gateway=values[3])
        elif cat == 'ROUTER':
            create_router(name=values[0])
            for i in range(int(values[1])):
                ip=values[(i+1)*2+1].split('/')
                add_interface(name=values[0], mac=values[(i+1)*2], ip=ip[0], mask=ip[1])
        elif cat == 'ROUTERTABLE':
            ip=values[1].split('/')
            add_routing_entry(name=values[0], ip=ip[0], mask=ip[1], nexthop=values[2], port=values[3])

def create_node(name, mac, ip, mask, gateway):
    node = Node(name, mac, ip, mask, gateway)
    nodes[name] = node

def create_router(name):
    router = Router(name)
    routers[name] = router

def add_interface(name, mac, ip, mask):
    router = routers[name]
    router.add_interface(mac, ip, mask)

def add_routing_entry(name, ip, mask, nexthop, port):
    print "Added entry on routing table from router {} from IP {}/{} to IP {} on port {}".format(name, ip, mask, nexthop, port)

class Node:
    name = ''
    mac = ''
    ip = ()
    gateway = ''
    ttl = 8
    arp_table = {}

    def __init__(self, name, mac, ip, mask, gateway):
        self.name = name
        self.mac = mac
        self.ip = (ip,mask)
        self.gateway = gateway


class Router:
    name = ''
    mac = ''
    ip = ''

    def __init__(self, name):
        self.name = name

    def add_interface(self, mac, ip, mask):
        self.mac = mac
        self.ip = (ip, mask)

    def foo(self):
    	pass