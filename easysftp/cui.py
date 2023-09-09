# Console UI for easysftp
# Version: 2.0.0

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
def progressBar(thread, queue, actionName):
    k = 0
    s = set()
    progress = 0
    while progress != 100:
        progress = queue.get()
        if progress not in s:
            print('\b'*40, end='', flush=True)
            if progress <= 33: setColor(red)
            elif progress <= 66: setColor(orange)
            elif progress == 100: setColor(green)
            else: setColor(cyan)
            print('{} ['.format(actionName), '-'*(progress//10), ' '*(10-(progress//10)), '] ', progress, '%', ' [{}]'.format(lAIcons[k]), end= '', sep = '', flush=True)
            s.add(progress)
            k = k+1 if k < len(lAIcons)-1 else 0
    setColor()
    return 0