class A(object):
    def __init__(self):
        pass

class B(A):
    def __init__(self):
        pass


import inspect
from pprint import pprint as pp

myobj = B

pp(inspect.getclasstree(inspect.getmro(myobj)))

