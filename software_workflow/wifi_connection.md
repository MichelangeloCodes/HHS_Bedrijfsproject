Instructions to find a devices on wifi and connect remote (ssh) to device.


Scan devices on the same wifi - should be a standard linux package
- ip a

should found something like the following:
inet 192.168.89.204/24 brd 192.168.89.255


Then, run nmap scan:
- sudo nmap -sn 192.168.89.0/24


output should be look something like:

Starting Nmap 7.95 ( https://nmap.org ) at 2024-10-10 20:22 CEST
Nmap scan report for 192.168.89.27
Host is up (0.27s latency).
MAC Address: B8:27:EB:93:BB:03 (Raspberry Pi Foundation)
Nmap scan report for 192.168.89.44
Host is up (0.069s latency).
MAC Address: EA:CC:EC:7B:24:DE (Unknown)
Nmap scan report for 192.168.89.204
Host is up.
Nmap done: 256 IP addresses (3 hosts up) scanned in 7.91 seconds

the ip is visible for the device we are searching (Raspberry Pi Foundation).


double check with ping to the device.
- sudo nmap -sn 192.168.89.27


connect to device with ssh:
- ssh <hostname@ip>

if it is the first time, expect a prompt about fingerpinting and accept it.
Then fill credentials in and you should connect to the deivce.

