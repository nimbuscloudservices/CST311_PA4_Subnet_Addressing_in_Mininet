#!/usr/bin/python
"""
Team Programming Assignment #4 Subnet Addressing In Mininet
Changelog:
- Moved S2 and S1 instantiation lines before R5 instantiation to revolve runtime errors.
-
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

__author__ = "Layla Gallez, Saul Mendoza-Loera, Yavik Kapadia"
__credits__ = ["Layla Gallez", "Saul Mendoza-Loera", "Yavik Kapadia"]
__status__ = "Prototype"
__date__ = "June 2nd, 2022"

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.10.0/24')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    # moved s2 and s1 above r5
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    
    # added IP to r5
    # added static route to r4 from r5
    r5 = net.addHost('r5', cls=Node, ip='10.0.20.1/24')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')
    r5.cmd('ip route add 192.168.30.1/30 via 10.0.20.1/24 r4')
    
    # added IP to r4
    # added static routes to r3 and r5 from r4
    r4 = net.addHost('r4', cls=Node, ip='192.168.30.1/30')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4.cmd('ip route add 10.0.10.1/24 via 192.168.30.1/30 r3')
    r4.cmd('ip route add 10.0.20.1/24 via 192.168.30.1/30 r5')
    
    # added IP to r3
    # added static route to r4 from r3
    r3 = net.addHost('r3', cls=Node, ip='10.0.10.1/24')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3.cmd('ip route add 10.0.10.2/24 via 10.0.10.1/24 h1')


    info( '*** Add hosts\n')
    # added IP to h1 and the default route of r3
    # added static route to r3 from h1
    h1 = net.addHost( 'h1', cls=Host, ip='10.0.10.2/24', 
                      defaultRoute='10.0.10.1')
    h1.cmd('ip route add 10.0.10.1/24 via 10.0.10.2/24 r3')
    
    # added IP to h2 and the default route of r3
    # added static route to r3 from h2
    h2 = net.addHost( 'h2', cls=Host, ip='10.0.20.3/24', 
                      defaultRoute='10.0.10.1')
    h2.cmd('ip route add 10.0.10.1/24 via 10.0.10.3/24 r3')
    
    # added IP to h3 and the default route of r5
    # added static route to r5 from h3
    h3 = net.addHost( 'h1', cls=Host, ip='10.0.20.2/24', 
                      defaultRoute='10.0.20.1')
    h3.cmd('ip route add 10.0.20.1/24 via 10.0.20.2/24 r5')
    
    # added IP to h4 and the default route of r5
    # added static route to r5 from h4
    h4 = net.addHost( 'h2', cls=Host, ip='10.0.20.3/24', 
                      defaultRoute='10.0.20.1')
    h4.cmd('ip route add 10.0.20.1/24 via 10.0.20.3/24 r5')


    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(s2, r5)
    net.addLink(s1, r3)
    
    # added intfName1 of r3 and params1 of r3's IP
    # added intfName2 of r4 and params2 of r4's IP
    net.addLink( r3, r4, intfName1='r3', 
                 params1={ 'ip' : '10.0.10.1/24' },
                         intfName2='r4', 
                 params2={ 'ip' : '192.168.30.1/30' } )
    
    # added intfName1 of r4 and params1 of r4's IP
    # added intfName2 of r5 and params2 of r5's IP
    net.addLink(r4, r5,  intfName3='r4', 
                 params3={ 'ip' : '192.168.30.1/30' },
                         intfName4='r5', 
                 params4={ 'ip' : '10.0.20.1/24' } )

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')

    # [Changelog] added cmd to start webserver on
    h2.cmd("python3 web_server.py")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()