import pytest
import random
import string
import math
import time
from decorators import *


def test_odd_sec_1():

    @only_odd
    def add(a, b):
        pass

    ret1 = add(1, 2)
    time.sleep(1)
    ret2 = add(1, 2)

    assert ('executed successfully' in ret1 and 'NOT executed' in ret2) or \
        ('executed successfully' in ret2 and 'NOT executed' in ret1)


##########################################################

def test_odd_sec_2():

    @only_odd
    def printme(*args):
        print(*args)

    ret1 = printme('hello', 'there')
    time.sleep(1)
    ret2 = printme('hello')

    assert ('executed successfully' in ret1 and 'NOT executed' in ret2) or \
        ('executed successfully' in ret2 and 'NOT executed' in ret1)


##########################################################

def test_logged():

    @logger
    def printme(*args):
        print(*args)

    ret1 = printme('hello', 'there')
    assert (': was called at time' in ret1)

    ret1 = printme()
    assert (': was called at time' in ret1)

    ret1 = printme()
    assert not('wrapper: was called at time' in ret1)

 ##########################################################


def test_timed_n():

    @timed_n(10)
    def printme(*args):
        print(*args)

    ret1 = printme('hello', 'there')
    ret1 = ret1.split(':')
    assert float(ret1[0]) > 0 and ret1[1] == 'printme()' and int(ret1[2]) == 10


##########################################################

def test_timed_n_2():

    @timed_n(-1)
    def printme(*args):
        pass

    with pytest.raises(ValueError):
        printme('hello', 'there')


##########################################################

def test_authenticatedOrNot_Authorized():

    @authenticatedOrNot(False)
    def printme1(*args):
        pass

    assert 'You are NOT AUTHENTICATED !!' in printme1('hello', 'there')[1]

##########################################################


def test_authenticatedOrNot_NotAuthorized():

    @authenticatedOrNot(True)
    def printme2(*args):
        pass

    assert 'You are AUTHENTICATED !!' in printme2('hello', 'there')[1]

##########################################################


def test_auth_factory():
    @auth_factory('high')
    def createfile(filename):
        print('success: created a file ', filename)

    def createfolder(filename):
        print('success: created a file ', filename)

    def editfile(filename):
        print('success: created a file ', filename)

    def readfile(filename):
        print('success: created a file ', filename)

    print(createfile('a.txt'))

    @auth_factory('low')
    def createfolder(filename):
        print('success: created a file ', filename)

    print(createfolder('a.txt'))
