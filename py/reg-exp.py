"""Python version regular expression.

The examples are from: https://www.topcoder.com/community/data-science/data-science-tutorials/using-regular-expressions-2/
"""


import re


def test(pattern, input, exp_match, exp_search, exp_findall):
    """test.

    re.match():  whole match
    re.search():  get first match
    re.findall():  get all matches
    """

    n = re.compile(pattern).groups
    print n

    matchObj = re.match(pattern, input, re.M|re.I)
    if matchObj:
        print 'match --> matchObj.group() : '
        for i in range(n):
            print matchObj.group(i)
        assert matchObj.group() == exp_match
    else:
        print 'No match!!'
        assert exp_match is None

    searchObj = re.search(pattern, input, re.M|re.I)
    if searchObj:
        print 'search --> searchObj.group() : ',
        for i in range(n):
            print searchObj.group(i)
        assert searchObj.group() == exp_search
    else:
        print 'search: Nothing found!!'
        assert exp_search is None

    findObj = re.findall(pattern, input, re.M|re.I)
    if findObj:
        print 'find --> findObj.group() : ', findObj
        assert findObj == exp_findall
    else:
        print 'findall: Nothing found!!'
        assert exp_findall is None
        

# The format is: pattern, input, re.match(), re.search(), re.findall().
cases = [(r'the|top|coder', 'Marius is one of tha topcoders.',
          None, 'top', ['top', 'coder']),
         (r'(top|coder)+', 'This regex matches topcoder and also codertop.',
          None, 'topcoder', ['coder', 'top']),
         (r'1{2,4}', '101 + 10 = 111 , 11111 = 10000 + 1111',
          None, '111', ['111', '1111', '1111']),
         (r'([a-z]+).\1', 'helloahelloatop-top,coder|coder',
          'helloahello', 'helloahello', ['hello', 'top', 'coder']),
         (r'[^b-d]at', 'hat',
          'hat', 'hat', ['hat']),
         (r'[^b-d]at', 'bat',
          None, None, None),
         (r'<([a-zA-Z][a-zA-Z0-9]*)(()| [^>]*)>(.*)</\1>',
          '<font size="2">Topcoder is the</font> <b>best</b>',
          '<font size="2">Topcoder is the</font>',
          '<font size="2">Topcoder is the</font>', 
          [('font', ' size="2"', '', 'Topcoder is the'), ('b', '', '', 'best')])]

for (pattern, input, exp_match, exp_search, exp_findall) in cases:
    print '\n** CASE:  pattern: <', pattern, '> input: <', input, '>'
    test(pattern, input, exp_match, exp_search, exp_findall)

print '\n PASS \n'
