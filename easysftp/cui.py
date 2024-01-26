# Console UI for easysftp
# Version: 2.6.1
# Last Updated: 26-01-2024


from queue import SimpleQueue
from time import time, strftime
from os import get_terminal_size

# ASCII Color Codes
red = '\033[31m'
green = '\033[32m'
yellow = '\033[93m'
blue = '\033[34m'
cyan = '\033[36m'
orange = '\033[33m'
reset = '\033[0m'

# Events
events = {
    '0101': ["\nHappy New Year {}!\n", red], 
    '0506': ["\nHey! It's World Environment Day! Don't forget to plant a tree!\n", green],
    '0808': ["\nMeow\n", orange],
    '2512': ["\nMerry Christmas!\n", cyan], 
    }

# Loading Animation Characters
lAIcons = ['|', '/', '-', '\\']

# Progress Bar Queue
queue = SimpleQueue()

# License
licenseInfo = '''
\neasysftp 2.6.0  Copyright (C) 2024  DAWN/ペンギン
This program comes with ABSOLUTELY NO WARRANTY; for details type `licenseinfo'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `licenseinfo' for details.
\n'''

# DAWN Logo
logo = '''
>>>>>>>>>>  >>>>          >>              >>              >>  >>>>        >>
>>>>    >>    >>>>         >>            >>>>            >>   >> >>       >>
>>>>    >>      >>>>        >>          >>  >>          >>    >>  >>      >>
>>>>    >>        >>>>       >>        >>    >>        >>     >>   >>     >>
>>>>    >>          >>>>      >>      >>      >>      >>      >>    >>    >>
>>>>    >>        >>>>         >>    >>        >>    >>       >>     >>   >>
>>>>    >>      >>>>            >>  >>          >>  >>        >>      >>  >>
>>>>    >>    >>>>               >>>>            >>>>         >>       >> >>
>>>>>>>>>>  >>>>                  >>              >>          >>        >>>>
'''

# Progress Bar Size
prgSize = 79


# Simple function to change console color
def setColor(color = reset):
    print(color, end='', flush=True)


def unitCalc(bytes): 
    bytes /= 1024
    if bytes >= 1024:
        bytes /= 1024
        if bytes >= 1024:
            return (bytes/1024, 'GB')
        else:
            return (bytes, 'MB')
    return (bytes, 'KB')


def eventCheck():
    date = strftime("%d%m")
    for i in events:
        if date == i:
            print("\n", strftime("%c"))
            print(events[i][1], events[i][0].format(strftime("%Y")), reset, sep = '')
    print('\n')
    return 0


# Progress Bar
def progressBar(thread, fname, action):
    global queue
    pT = time()
    sT = time()
    k, ft = 0, 0
    fname  = ' '*20+fname+' '*20
    s, e = 0, 20
    spd = [0, 'MB'] # Starting Speed set at 0 MB/s
    progress = [0, 2] # Starting Progress set at 0/2 (To avoid errors in case of queue delay)
    c = (get_terminal_size()[0] - prgSize)
    ic = '▼' if action == 'D' else '▲'

    while thread.is_alive() or (progress[0]/progress[1] != 1):
        prg = int((progress[0]/progress[1])*100)

        try:
            progress = list(queue.get_nowait())
        except:
            progress = progress
        
        print('\b'*(c+prgSize)*2, end='', flush=True)
        if prg <= 33: setColor(red)
        elif prg <= 66: setColor(orange)
        elif prg == 100: setColor(green)
        else: setColor(cyan)

        
        i, f = unitCalc(progress[0]), unitCalc(progress[1])

        #Time Counters
        if (time() - sT) >= 1: #Speed Calculation
            spd = unitCalc((progress[0] - ft)/(time() - sT))
            sT = time()
            ft = progress[0]
            

        if time() - pT > 0.1: #Progress Bar UI
            k = k+1 if k < len(lAIcons)-1 else 0
            pT = time()
            t = len(fname)
            s = s+1 if e < t else 0
            e = e+1 if e < t else 20

        if prg == 100: s,e = 20, 40

        percent = str(prg)+'%'
        bar = '/'*((c*prg//100)-1) + '{}'.format(lAIcons[k]) +' '*(c-(c*prg//100))
        bytesDownloaded = '{:.2f}'.format(i[0]) + ' {}'.format(i[1]) + ' / ' + '{:.2f}'.format(f[0]) + ' {}'.format(f[1])
        speed = '{:.2f}'.format(spd[0]) + ' ' + spd[1] + '/s'
        #output = '{:^20}\t'.format(fname[s:e]) + bar + bytesDownloaded + percent + speed + '\t' + ic
        output = '{:20}   [{:<}]  {:23}    {:^12}    [{:^4}] {:>}'.format(fname[s:e], bar, bytesDownloaded, speed, percent, ic)
        print(output,  end= '', flush=True)
        
    setColor()
    return 0