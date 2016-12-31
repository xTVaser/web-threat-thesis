import re

test = '{0:08b}'.format(10)

string = '/test/website/?username=<A+HREF="h+tt+p://6&#09;6.000146.0x7.147/">XSS</A>&password=<A+HREF="h+tt+p://6&#09;6.000146.0x7.147/">XSS</A>&name=<A+HREF="h+tt+p://6&#09;6.000146.0x7.147/">XSS</A>&'

fields = re.compile("(\?|&)[\w\d]+=").split(string)

del fields[1::2]

print("ye")