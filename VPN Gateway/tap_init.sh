#!/bin/bash
#Generic script for OpenWRT routers connection to L2 OpenVPN network with inner DHCP
openvpn --mktun --dev tap0
ifconfig tap0 0.0.0.0 promisc up
ifconfig br-lan down
brctl addif br-lan tap0
brctl show
ifconfig br-lan 0.0.0.0 promisc up
#%config% chould be replaced by name of .ovpn file for given device
openvpn --config /root/%config%.ovpn
