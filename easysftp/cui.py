# Console UI for easysftp
# Version: 2.2.0
# Last Updated: 28-12-2023


from time import time
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


# Progress Bar
def progressBar(thread, actionName):
    global queue
    k, progress = 0, 0
    t = time()
    c, l = get_terminal_size()
    c -= (len(actionName) + 12)
    while thread.is_alive() and progress != 100:
        progress = queue.get()
        print('\b'*c*2, end='', flush=True)
        if progress <= 33: setColor(red)
        elif progress <= 66: setColor(orange)
        elif progress == 100: setColor(green)
        else: setColor(cyan)
        print('{} ['.format(actionName), '-'*(c*progress//100), ' '*(c-(c*progress//100)), '] ', progress, '%', ' [{}]'.format(lAIcons[k]), end= '', sep = '', flush=True)
        if time() - t > 0.1: k = k+1 if k < len(lAIcons)-1 else 0
        t = time() if (time() - t > 0.1) else t
    setColor()
    return 0