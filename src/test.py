import os
from subprocess import Popen, PIPE

cmd = '/Users/lukashavrlant/Python/fca-search/src/search '
fun = lambda dtb, q: os.popen(cmd + '-d ' + dtb + ' -q "' + q + '"')
stream = fun('matweb', 'derivace')
#print(stream.read())


print(Popen("/Users/lukashavrlant/Python/fca-search/src/search -d matweb -q derivace nt", stdout=PIPE, shell=True).stdout.read())
#stream = os.popen("some_command with args")