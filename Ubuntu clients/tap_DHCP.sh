#!/bin/bash
#

[ -x /sbin/dhclient ] || exit 0

case $script_type in

up)
# echo "Your misson should you choose to accept it, is to open a new terminal and issue:"
# echo "dhclient -v ${dev}"
# echo "You have 30 seconds...GO!"
dhclient -v "${dev}" &
;;
down)
echo "Releasing ${dev} DHCP lease."
dhclient -r "${dev}"
;;
esac

#following lines should be added in .ovpn file
#script-security 2
#route-delay 10
#up /etc/openvpn/dhcp.sh
#down-pre
#down /etc/openvpn/dhcp.sh
