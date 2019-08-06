#!/usr/bin/env python3

import pyfortiapi
import sys
import pprint
import itertools
import argparse
import getpass
import time
import ipaddress
import paramiko

def set_ip(addr):
    try :
        ipaddr = ipaddress.IPv4Interface(addr)
        ip_pref = str(ipaddr.with_prefixlen)
        ip_netmsk = str(ipaddr.with_netmask)
        ip_pref = ip_pref.split("/")
        ip_netmsk = ip_netmsk.split("/")
        return (ip_pref,ip_netmsk)
        
    except Exception as e:
        print(addr,'does not appear to be an IPv4 or IPv6 address')
        exit(1)

def validate_ip4(addr):
    try:
        ipaddress.IPv4Interface(addr)
    
    except Exception as e:
        print(addr,'does not appear to be an IPv4 or IPv6 address')
        exit(1)

''' This function creates the ssh connection session'''
def sshconnect(host,user,password):
    host = host
    username = user
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)
        fgtssh = ssh.invoke_shell()       
        return fgtssh

    except Exception as e:
        raise(e)

''' This function creates the api connection session'''
def connect(host,user,password):
    host = host
    user = user
    fgsession = fgt.FortiGate(ipaddr=host,username=user,password=password)
    try:
        return fgsession

    except Exception as e:
        raise(e)

#''' This function updates a named address group members with a new member'''
#def upd_address_group(group,member):
#    data = "{'member': [{'name': '" + str(member) + "'}]}"
#    updategroup = fgtsession.update_address_group(group,repr(data))
#    pprint.pprint('Return status of process was'+str(updategroup))
#    return(updategroup)

''' This function updates a named address group members with a new member via ssh'''
def ssh_upd_address_group(group,member):
    fgtsshsession.send('config firewall addrgrp'+'\n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    fgtsshsession.send('edit ' + group +' \n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    fgtsshsession.send('append member '+member+'\n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    fgtsshsession.send('end'+'\n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    
''' This function deletes an address group member from an named address group'''
def del_address_group(group,member):
    group = group
    member = member
    list_group = fgtsession.get_address_group(group)
    addr_str = ''
    
    for i in list_group:
        member_list = i['member']
    
    for j in member_list:
        name = j['name']
        if name == member:
            pass
        else:
            addr_str = addr_str+" "+name
    
    fgtsshsession.send('config firewall addrgrp'+'\n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    fgtsshsession.send('edit '+group+' \n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    fgtsshsession.send('set member'+addr_str+'\n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    fgtsshsession.send('end'+'\n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    return(True)

'''This was the code for the http api version
    list_group = fgtsession.get_address_group(group)
    addr_str = ''
    for i in list_group:
        member_list = i['member']
        for j in member_list:
            if j["name"] == member: #/this was intented using the api
                member_list.remove(j) #/this was intednted using the api too
    #print(addr_str)
    #print(member_list)
    #new_member_dict = {}
    #new_member_dict['member'] = member_list
    #updategroup = fgtsession.update_address_group(group,repr(new_member_dict))
    #pprint.pprint('Return status of process was '+str(updategroup))
    #return(updategroup) 
'''

''' This function lists all objects and their network info on the given address group.'''
def list_ips(group):
    list_group = fgtsession.get_address_group(group)
    for i in list_group:
        member_list = i['member']
        for dict in member_list:
            name = dict['name']
            addr = fgtsession.get_firewall_address(name)
            for item in addr:
                ip = item['start-ip']
                mask = item['end-ip']
            final = "Object: " + str(name) + " " + "IP: " + str(ip) + " " + "Mask: "  + str(mask)
            print(final)
    
''' This function creates a new address object '''
def create_addr_name_firewall_obj(name,address):
    addr_obj_name = name
    addr = set_ip(address)
    addr = addr[1]
    adr = addr[0]
    mas = addr[1]
    #addrmsk = adr+" "+mas
    fgtsshsession.send('config firewall address'+'\n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    fgtsshsession.send('edit ' + addr_obj_name +' \n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    fgtsshsession.send('set subnet '+adr+" "+mas+'\n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    fgtsshsession.send('end'+'\n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    return(True)
   
    ''' This code is for api use not used for ssh
    #data = "{'name': "+"'"+name+"'"+", 'type': 'subnet', 'subnet': "+"'"+addrmsk+"'"+"}"
    #do = fgtsession.create_firewall_address(name,data)
    #return(do)
    '''

''' This function deletes a firewall address object'''
def del_addr_name_fw_obj(name):
    obj_name = name
    fgtsshsession.send('config firewall address'+'\n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    fgtsshsession.send('delete '+obj_name+' \n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    fgtsshsession.send('end'+'\n')
    time.sleep(0.5)
    print(fgtsshsession.recv(2048))
    return(True)

def help():
    pass

if __name__ == '__main__':
    fgt = pyfortiapi
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--passwd',type=str,required=False)
    parser.add_argument('-u','--user',type=str,required=True)
    parser.add_argument('-fgt','--fortigate_ip',type=str,required=True)
    parser.add_argument('-b','--block', type=str)
    parser.add_argument('-r','--remove_block', type=str) 
    parser.add_argument('-g','--address_group_name', type=str,default='blocklist')
    parser.add_argument('-n','--address_name',type=str) 
    parser.add_argument('-l','--list_blocked_ips', action="store_true") 
    args = parser.parse_args()

    passwd = args.passwd
    user = args.user
    fgtip = args.fortigate_ip
    blockip = args.block
    allowip = args.remove_block
    addrgrp_name = args.address_group_name
    list_blockd = args.list_blocked_ips
    addrname = args.address_name

    for i in blockip,fgtip:
        if i == None:
            pass
    
        else:
            validate_ip4(i)

    if passwd == None:
        #password = "whatever"
        passwd = getpass.getpass('Enter password for user ' + user + '\n')
    
    else:
        pass 

    if list_blockd is True:
        try:
           fgtsession = connect(fgtip,user,passwd)
           list_ips(addrgrp_name)
           exit(0)
    
        except Exception as e:
            raise(e)

    elif blockip is not None and addrname is not None:
        try:
            fgtsession = connect(fgtip,user,passwd)
            fgtsshsession = sshconnect(fgtip,user,passwd)
            create_addr_name_firewall_obj(addrname,blockip)
            ssh_upd_address_group(addrgrp_name,addrname)
            exit(0)
        
        except Exception as f:
            raise(f)
    
    elif allowip is not None and addrgrp_name is not None:
        try:
            fgtsession = connect(fgtip,user,passwd)
            fgtsshsession = sshconnect(fgtip,user,passwd)
            del_address_group(addrgrp_name,allowip)
            del_addr_name_fw_obj(allowip)
            exit(0)
        
        except Exception as k:
            raise(k)

    exit(0)

'''Some functions tests below'''
'''fgtsession = connect(args.fortigate_ip,args.user,args.passwd)
   fgtsshsession = sshconnect(args.fortigate_ip,args.user,args.passwd)'''

'''
    fgtsshsession = sshconnect('1.1.1.1','user','pass')
    fgtsession = connect('1.1.1.1','user','pass')
    create_addr_name_firewall_obj('scoobydoo_blocklist','169.254.253.0/24')
    time.sleep(2)
    print('\n')
    ssh_upd_address_group('blocklist','scoobydoo_blocklist')
    time.sleep(2)
    print('\n')
    list_ips('blocklist')
    time.sleep(2)
    print('\n')
    del_address_group('blocklist','scoobydoo_blocklist')
    time.sleep(2)
    print('\n')
    list_ips('blocklist')
    time.sleep(2)
    print('\n')
    del_addr_name_fw_obj('scoobydoo_blocklist')
    exit()
'''