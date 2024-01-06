# Console UI for easysftp
# Version: 2.5.0
# Last Updated: 06-01-2024


from time import ctime, time
from queue import SimpleQueue
from os import get_terminal_size


# ASCII Color Codes
red = '\033[31m'
green = '\033[32m'
yellow = '\033[93m'
blue = '\033[34m'
cyan = '\033[36m'
orange = '\033[33m'
reset = '\033[0m'

# Loading Animation Characters
lAIcons = ['|', '/', '-', '\\']

# Progress Bar Queue
queue = SimpleQueue()

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


# Simple function to change console color
def setColor(color = reset):
    print(color, end='', flush=True)


def unitCalc(bytes): 
    bytes /= 1024
    if bytes >= 1024:
        bytes /= 1024
        if bytes >= 1024:
            return (str(round(bytes/1024, 2)), 'GB')
        else:
            return (str(round(bytes, 2)), 'MB')
    return (str(round(bytes, 2)), 'KB')


def eventCheck():
    t = ctime()
    t = t.split()
    if t[1] == 'Jan' and t[2] == '01':
        print('\n', t)
        print(red, '\nHappy New Year {}!\n'.format(t[4]), reset, sep='')
    if t[1] == 'Dec' and t[2] == '25':
        print('\n', t)
        print(cyan, '\nMerry Christmas!\n', reset, sep='')
    if t[1] == 'Jun' and t[2] == '5':
        print('\n', t)
        print(green, "\nHey! It's World Environment Day! Don't forget to plant a tree!\n", reset, sep='')
    print('\n')


# Progress Bar
def progressBar(thread, actionName):
    global queue
    t = time()
    sT = time()
    k, ft = 0, 0
    spd = ['0', 'MB']
    progress = [1, 2]
    c, l = get_terminal_size()
    c -= (len(actionName) + 42)
    ic = '▼' if actionName[0] == 'D' else '▲'
    while thread.is_alive() or (progress[0]/progress[1] != 1):
        prg = int((progress[0]/progress[1])*100)
        try:
            progress = list(queue.get_nowait())
        except:
            progress = progress
        print('\b'*c*2, end='', flush=True)
        if prg <= 33: setColor(red)
        elif prg <= 66: setColor(orange)
        elif prg == 100: setColor(green)
        else: setColor(cyan)
        percent = str(prg)+'% '
        i, f= unitCalc(progress[0]), unitCalc(progress[1])
        if (time() - sT) >= 1:
            spd = unitCalc((progress[0] - ft)/(time() - sT))
            sT = time()
            ft = progress[0]
        bar = '[' + '/'*((c*prg//100)-1) + '{}'.format(lAIcons[k]) +' '*(c-(c*prg//100)) + '] '
        bytesDownloaded = i[0] + ' {}'.format(i[1]) + ' / ' + f[0] + ' {} '.format(f[1])
        speed = spd[0] + ' ' + spd[1] + '/s '
        output = '{} '.format(actionName) + bar + bytesDownloaded + percent + speed + '\t' + ic
        print(output,  end= '', flush=True)
        if time() - t > 0.1: k = k+1 if k < len(lAIcons)-1 else 0
        t = time() if (time() - t > 0.1) else t
    setColor()
    return 0