#!/usr/bin/python
"""
Team Programming Assignment #4 Subnet Addressing In Mininet
Team 5 Layla, Saul, Yavik
"""
import subprocess

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from mininet.term import makeTerm
import time

__author__ = "Layla Gallez, Saul Mendoza-Loera, Yavik Kapadia"
__credits__ = ["Layla Gallez", "Saul Mendoza-Loera", "Yavik Kapadia"]
__status__ = "Prototype"
__date__ = "June 2nd, 2022"


def myNetwork():
    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/24')

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6633)

    info('*** Add switches\n')
    # [Changelog] moved s2 and s1 above r5
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    # [Changelog] added IP to r5
    r5 = net.addHost('r5', cls=Node, ip='10.0.2.1/24')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')

    # [Changelog] added IP to r4
    r4 = net.addHost('r4', cls=Node, ip='192.168.1.2/30')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')

    # [Changelog] added IP to r3
    r3 = net.addHost('r3', cls=Node, ip='10.0.1.1/24')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Add hosts\n')

    # [Changelog] added IP to h1 and the default route of r3
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.50/24',
                     defaultRoute='via 10.0.1.1')

    # [Changelog] added IP to h2 and the default route of r3
    h2 = net.addHost('h2', cls=Host, ip='10.0.1.100/24',
                     defaultRoute='via 10.0.1.1')

    # [Changelog] added IP to h3 and the default route of r5
    h3 = net.addHost('h3', cls=Host, ip='10.0.2.100/24',
                     defaultRoute='via 10.0.2.1')

    # [Changelog] added IP to h4 and the default route of r5
    h4 = net.addHost('h4', cls=Host, ip='10.0.2.50/24',
                     defaultRoute='via 10.0.2.1')

    info('*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(s2, r5)
    net.addLink(s1, r3)

    # [Changelog] added IP address to r3-eth1
    net.addLink(r3, r4, intfName1='r3-eth1',
                params1={'ip': '192.168.1.1/30'})

    # [Changelog] added IP address to r4-eth1 and r5-eth1
    net.addLink(r4, r5, intfName1='r4-eth1',
                params1={'ip': '192.168.1.5/30'},
                intfName2='r5-eth1',
                params2={'ip': '192.168.1.6/30'})

    info('*** Starting network\n')
    net.build()

    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info('*** Post configure switches and hosts\n')

    info('*** Adding static routes for r3, r4, r5\n')

    # [Changelog] added route to 10.0.2.0/24 and 192.168.1.4/30
    r3.cmd('ip route add 10.0.2.0/24 via 192.168.1.2 dev r3-eth1')
    r3.cmd('ip route add 192.168.1.4/30 via 192.168.1.2 dev r3-eth1')

    # [Changelog] added route to 10.0.2.0/24 and 10.0.1.0/24
    r4.cmd('ip route add 10.0.2.0/24 via 192.168.1.6 dev r4-eth1')
    r4.cmd('ip route add 10.0.1.0/24 via 192.168.1.1 dev r4-eth0')

    # [Changelog] added route to 10.0.1.0/24 and 192.168.1.0/30
    r5.cmd('ip route add 10.0.1.0/24 via 192.168.1.5 dev r5-eth1')
    r5.cmd('ip route add 192.168.1.0/30 via 192.168.1.5 dev r5-eth1')

    # start h1, h2, h3, h4 terminals
    subprocess.call(["sh", "PA4_Gallez_Kapadia_Mendoza-Loera_chat_cert.sh"])
    chatServer = makeTerm(h4, 'Chat Server', 'xterm', None, 'python3 PA4_Gallez_Kapadia_Mendoza-Loera_chat_server.py')
    tslwebServer = makeTerm(h2, 'TLS-enabled Simple Web Server', 'xterm', None, 'python3 PA4_Gallez_Kapadia_Mendoza-Loera_web_server.py')
    time.sleep(0.5)
    clientXChat = makeTerm(h1, 'Client Chat', 'xterm', None, 'python3 PA4_Gallez_Kapadia_Mendoza-Loera_chat_client.py')
    clientYChat = makeTerm(h3, 'Client Chat', 'xterm', None, 'python3 PA4_Gallez_Kapadia_Mendoza-Loera_chat_client.py')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
