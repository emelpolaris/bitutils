import pexpect
import re
import sys
import time
import traceback
from datetime import datetime
import getpass
import schedule

# configure options for your command
wallet = "JJcold"#"main-wallet"       # wallet name of your coldkey
# hotkeys = ["JJwarm", "JJhot", "JJa", "JJb", "JJc", "JJd", "JJe", "JJf", "JJg", "JJh", "JJi", "JJj"] #["mining-hotkey-2"]        # a list with the names of all the hotkeys you want to register
hotkeys = ["JJd"]
netuid = int(input('Subnet ID: '))                        # subnet uid you want to register
highest_cost = float(input('Max registration fee: '))                # the maximal amount of tao you are willing to burn to register
# print('Type in your password:')
password = str(getpass.getpass('Type in your password:'))        # password for your coldkey
# iterate = True 

# start registraion bot

def my_task():
    iterate = True 

    while True:
        for hotkey in hotkeys:
            while iterate:
                try:
                    command = 'btcli subnet register --subtensor.network finney --netuid {} --wallet.name {} --wallet.hotkey {}'.format(netuid, wallet, hotkey)
                    
                    # Format the time as HH:MM:SS
                    formatted_time = datetime.now().time().strftime("%H:%M:%S")
                    
                    # Print the formatted time
                    print("\nColdkey: ", wallet, "\nHotkey: ", hotkey, flush=True)
                    print(formatted_time, flush=True)
                    child = pexpect.spawn(command)

                    child.logfile_read = sys.stdout.buffer
                    
                    try:
                        child.expect(r'The cost to register by recycle is (.*?)(?:\n|$)')
                    except Exception as e:
                        # print("An error occured", e)
                        # child.expect(r'Insufficient balance τ(.*) to register neuron. Current recycle is τ(.*) TAO\n')
                        break
                    cost_str = child.match.group(1).decode('utf-8').replace('τ', '')
                    clean_cost_str = re.sub(r'\x1b\[[0-9;]*m', '', cost_str).strip()
                    cost = float(clean_cost_str)
                    
                    if cost > highest_cost:
                        child.sendline('n')
                        print("Not registering:", flush=True)
                        continue
                    else:
                        child.sendline('y')
                        print("sending y to register", flush=True)
                    
                    child.expect('Enter password to unlock key')
                    child.sendline(password)
                    # print("\nPassword sent")
                    try:
                        child.expect(r'Recycle (.*?) to register on subnet')
                    except:
                        break
                        
                    recycle_cost_str = child.match.group(1).decode('utf-8').replace('τ', '')
                    clean_recycle_cost_str = re.sub(r'\x1b\[[0-9;]*m', '', recycle_cost_str).strip()
                    recycle_cost = float(clean_recycle_cost_str)
                    
                    if recycle_cost > highest_cost:
                        child.sendline('n')
                        print("Sending: n", flush=True)
                    else:
                        child.sendline('y')
                        print("Sending2: y", flush=True)
                        
                        try:
                            child.expect(r'Registered', timeout=120)
                            iterate = False
                        except:
                            print('Falied to register, trying again...')

                except Exception as e:
                    print("An error occured", e)
                    print(traceback.format_exc())
                    child.sendintr()             # Send Ctrl+C
                    child.expect(pexpect.EOF)    # Wait for the command to exit
                    if iterate:
                        break
                    else:
                        continue

schedule.every().day.at("03:30").do(my_task)
# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(10)
