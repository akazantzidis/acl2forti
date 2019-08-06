# acl2forti
Python program to automate Fortigate firewall blocklist

*** Something to know *** 

This program has something strange in there if you check the code.
It uses both fortiapi and paramiko libraries.That's because some 
functions are using Fortigate api and some others use ssh to access the device.
This is because at the time of writing, my actual device firmware did not
allowed me to change some settings via api,so i had to use ssh.The api fuctions are 
still there in the code,but are comment out.Feel free to use them,if you have newer
versions of fortigate firmware.
