red = '\033[31m'
green = '\033[32m'
yellow = '\033[93m'
blue = '\033[34m'
cyan = '\033[36m'
orange = '\033[33m'
reset = '\033[0m'


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


def setColor(color = reset):
    print(color, end='', flush=True)