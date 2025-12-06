# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 14:01:30 2024

@author: amrutnp
"""

import xml.etree.ElementTree as ET


# PWRON, PWROFF, USBON, USBOFF, EDLON, EDLOFF
# VOLUP, VOLDN, KYPD --> Key file
opcode_list = ['0'] * 9
ls = {}

file = 'cfg.xml'
mytree = ET.parse(file)
root = mytree.getroot()
for i in root:
    if i.tag == 'USBON':
        opcode_list[2] = i.text
        ls ['uy'] = i.text
    if i.tag == 'USBOFF':
        opcode_list[3] = i.text
        ls ['un'] = i.text
    if i.tag == 'PWROFF':
        opcode_list[1] = i.text
        ls ['pn'] = i.text
    if i.tag == 'PWRON':
        opcode_list[0] = i.text
        ls ['py'] = i.text
    if i.tag == 'EDLON':
        opcode_list[4] = i.text
        ls ['ey'] = i.text
    if i.tag == 'EDLOFF':
        opcode_list[5] = i.text
        ls ['en'] = i.text
    if i.tag == 'VOLP':
        opcode_list[6] = i.text
        ls ['vp'] = i.text
    if i.tag == 'VOLM':
        opcode_list[7] = i.text
        ls ['vm'] = i.text
    if i.tag == 'KYP':
        opcode_list[8] = i.text
        ls ['kp'] = i.text
        

if '0' in opcode_list:
    print ('Missing opcode in xml file')
    raise KeyboardInterrupt

# new_ls = []
for i in opcode_list:
    if len(i) != 4 :
        print ('Invalid opcode in xml file')
        raise KeyboardInterrupt
    # new_ls.append( [ int(i[:2],16), int(i[2:],16) ])        # hex conversion

# opcode_list = new_ls
