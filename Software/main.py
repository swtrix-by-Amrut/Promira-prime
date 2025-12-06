import serial
from serial.tools import list_ports
from ui import *
import sys, time
import random
# import threading


from datetime import date
today = date.today()
if today.year> 2025   :
    print("Deprecated warning::\npyserial library is outdated. Please reinstall pyserial from pip\n\n")
    raise SystemExit()


from read_xml import ls
        
        
if sys.version_info<(3,) :
    print ('Can\'t run on python 2.7\n Please run this program on version > 3.10')
    input('')
    raise SystemExit


ports = list(list_ports.comports())
selected = None
for p in ports:
    # print (p)
    if 'CH340' in str(p):
        selected = p

if selected == None:
    print ('Couldn\'t find any compatible COM port' )
    input('')
    raise SystemExit

comport = str(selected).split()[0]
port = serial.Serial( comport, baudrate =  115200,
                                 parity= serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 timeout=0, write_timeout=0)
#==============================================================================

time.sleep(3)
print ('done waiting')

port.write(b'~')
time.sleep(0.5)
port.reset_input_buffer()
port.reset_output_buffer()

rand = lambda: int (100 * random.random())
int2 = lambda x: int ( x, 16 ) 

backup_str = ''
def log(s):
    global backup_str
    a = dpg.get_value ('textEdit')
    dpg.set_value ('textEdit', a+ backup_str + s+'\n' )
    backup_str = ''

flush_var = True

with dpg.theme() as green:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 208, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0,0,0), category=dpg.mvThemeCat_Core)
with dpg.theme() as red:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (100, 100,100), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0,0,0), category=dpg.mvThemeCat_Core)

'''
def flush_serial_read():
    if port.isOpen() and flush_var== True:
        if port.in_waiting > 0:
            port.reset_input_buffer()
    # if port.in_waiting > 0 :
    #     ch = port.readline()
    #     print ( ch.decode() + '\n' )
    threading.Timer(0.1 , flush_serial_read).start()
'''

# flush_serial_read()



def read_(cmd):
    global flush_var 
    flush_var = False
    port.write(b'r '+str(cmd).encode('utf-8') +b'\n')
    count = 0
    while(count  == 0):
        if port.in_waiting > 0 :
            ch = port.readline()
            # print ( ch.decode() , end = '' )
            count += 1
    flush_var = True
    return  int2 (ch )    # convert HEX string to proper int

def toggle_PWR():
    global backup_str 
    backup_str = 'power '
    toggle_stuff(ls['py'], ls['pn'], 'pushButton', ls['pn'][:2] , ls['pn'][2:] )

def toggle_USB():
    global backup_str 
    backup_str = 'USB '
    toggle_stuff( ls['uy'], ls['un'], 'pushButton_2', ls['un'][:2] ,  ls['un'][2:])

def toggle_EDL():
    global backup_str 
    backup_str = 'EDL '
    toggle_stuff(ls['ey'], ls['en'], 'pushButton_9', ls['en'][:2], ls['en'][2:] )

def toggle_stuff(cmd1, cmd2, local_label, addr_read, offValue, mask = 0xFF):
    # port.reset_input_buffer()
    x= read_(addr_read)   # gives BCD number 
    if type (mask) == str : 
        mask = int2 (mask)
        cmd1 = hex ( int (cmd1 , 16 ) | mask | x)
        cmd2_1 = hex (( int (cmd2[2:] , 16 ) | x ) & ( 0xFF & ~mask ) ) 
        if len(cmd2_1) == 3:
            cmd2_2 = '0' + cmd2_1 [2:]
        else:
            cmd2_2 = cmd2_1
        cmd1, cmd2 = cmd1[2:] , cmd2 [:2]  + cmd2_2
        # print (mask, cmd1, cmd2)
        
    # port.reset_input_buffer()
    # port.reset_output_buffer()
    if x & mask == int2(offValue):
        port.write(b'w ' + cmd1.encode('utf-8') + b'\n')
        # dpg.configure_item(local_label, default_value =  "ON" )
        dpg.bind_item_theme(local_label ,green)
        log('ON')
    else:
        port.write(b'w ' + cmd2.encode('utf-8')+ b'\n')
        # dpg.configure_item(local_label, default_value =  "OFF"  )
        dpg.bind_item_theme(local_label ,red)
        log('OFF')
    port.reset_input_buffer()
    port.reset_output_buffer()

def checkStatus(local_label, addr_read ,offValue,  mask = 0xFF ):
    x= read_(addr_read)
    if type (mask) == str : 
        mask = int2 (mask)
    if x & mask == int2(offValue):
        dpg.bind_item_theme(local_label ,red)
    else:
        dpg.bind_item_theme(local_label ,green)

def Refresh_connection():
    num = rand()

    port.write(b'w 22'+ str(num).encode('utf-8') + b'\n')
    x= read_('22')
    print (x, num, end = '' )
    if x !=  int2(str(num)):
        print ('nk')
        dpg.configure_item('label_11', default_value =  "Not Connected"  )
        return
    else:
        print ('k')
        dpg.configure_item('label_11', default_value =  "Connected"  )
    checkStatus ('pushButton',   ls['pn'][:2],       ls['pn'][2:] )    #Power
    checkStatus ('pushButton_2', ls['un'][:2],       ls['un'][2:] )    #USB
    checkStatus ('pushButton_9', ls['en'][:2],       ls['en'][2:] )    #EDL
    checkStatus ('pushButton_3', ls['kp'][:2], '00', ls['kp'][2:] )    #KYPD
    checkStatus ('pushButton_4', ls['vp'][:2], '00', ls['vp'][2:] )    #VOLP
    checkStatus ('pushButton_5', ls['vm'][:2], '00', ls['vm'][2:] )    #VOLM

def toggle_KYPD():
    global backup_str 
    backup_str = 'KYPD '
    adr = ls['kp'][:2]
    toggle_stuff(adr+'00', adr+'00', 'pushButton_3', adr, '00', ls['kp'][2:] )
def toggle_volP():
    global backup_str 
    backup_str = 'VOLP ' 
    adr = ls['vp'][:2]    
    toggle_stuff(adr +'00', adr+'00', 'pushButton_4', adr , '00',  ls['vp'][2:] )
def toggle_volM():
    global backup_str 
    backup_str = 'VOLM '    
    adr = ls['vm'][:2]    
    toggle_stuff(adr+'00', adr+'00', 'pushButton_5', adr , '00', ls['vm'][2:] )


dpg.set_item_callback("pushButton"   , toggle_PWR)
dpg.set_item_callback("pushButton_2"   , toggle_USB)
dpg.set_item_callback("pushButton_3"   , toggle_KYPD)
dpg.set_item_callback("pushButton_4"   , toggle_volP)
dpg.set_item_callback("pushButton_5"   , toggle_volM)
dpg.set_item_callback("pushButton_9"   , toggle_EDL)

def seq_pon ():
    port.write(b'w '+ ls['pn'].encode('utf-8') +b'\n')
    port.write(b'w '+ ls['un'].encode('utf-8') +b'\n')
    port.write(b'w '+ ls['en'].encode('utf-8') +b'\n')
    time.sleep(0.3)
    port.write(b'w '+ ls['uy'].encode('utf-8') +b'\n')
    port.write(b'w '+ ls['py'].encode('utf-8') +b'\n')
    log(' Power Cycle Done')
    Refresh_connection()

def seq_poff ():
    port.write(b'w '+ ls['en'].encode('utf-8') +b'\n')
    port.write(b'w '+ ls['un'].encode('utf-8') +b'\n')
    port.write(b'w '+ ls['pn'].encode('utf-8') +b'\n')
    log('Device Powered OFF ')
    Refresh_connection()

def seq_edl ():
    port.write(b'w '+ ls['pn'].encode('utf-8') +b'\n')
    port.write(b'w '+ ls['un'].encode('utf-8') +b'\n')
    time.sleep(0.3)   
    port.write(b'w '+ ls['ey'].encode('utf-8') +b'\n')
    port.write(b'w '+ ls['uy'].encode('utf-8') +b'\n')
    port.write(b'w '+ ls['py'].encode('utf-8') +b'\n')
    log('EDL boot done')
    Refresh_connection()


def write_custom():
    a = dpg.get_value ('lineEdit')
    if len(a) < 4:
        log ('Incorrect opecode')
        return
    a= a[:4]
    try:
        b = int (a, 16 )
    except:
        log ('non-HEX input')
        return
    port.write(b'w ' + a.encode('utf-8')+ b'\n')
    log(f'Wrote {a}')
    Refresh_connection()

def read_custom ():
    a = dpg.get_value ('lineEdit')
    if len(a) < 2:
        log ('Incorrect opecode')
        return
    a= a[:2]
    try:
        b = int (a, 16 )
    except:
        log ('non-HEX input')
        return
    x= read_(a)
    log (f'value @{a}= ' + hex (x) )





dpg.set_item_callback("pushButton_6"   , seq_pon)
dpg.set_item_callback("pushButton_7"   , seq_poff)
dpg.set_item_callback("pushButton_8"   , seq_edl)
dpg.set_item_callback("pushButton_11"   , Refresh_connection)
dpg.set_item_callback("pushButton_13"   , write_custom)
dpg.set_item_callback("pushButton_14"   , read_custom)



Refresh_connection()







gui_kick_off()
# port .close()
