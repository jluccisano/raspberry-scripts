#!/usr/bin/python
#sudo pip install tqdm
from scripts.sprinkler.statemachine import StateMachine
from time import sleep
from tqdm import trange

def start():
    print "Starting scenario"
    return ("Zone A")

def runZoneA():
    print "Run zone: A"
    for i in trange(20, leave=True):
        sleep(0.1)
    return ("Zone B")

def runZoneB():
    print "Run zone: B "
    for i in trange(20, leave=True):
        sleep(0.1)
    return ("Zone C")

def runZoneC():
    print "Run zone: C "
    for i in trange(20, leave=True):
        sleep(0.1)
    return ("Zone D")

def runZoneD():
    print "Run zone: D "
    for i in trange(20, leave=True):
        sleep(0.1)
    return ("Zone E")

def runZoneE():
    print "Run zone: E "
    for i in trange(20, leave=True):
        sleep(0.1)
    return ("End")

if __name__== "__main__":
    m = StateMachine()
    m.add_state("Start", start)
    m.add_state("Zone A", runZoneA)
    m.add_state("Zone B", runZoneB)
    m.add_state("Zone C", runZoneC)
    m.add_state("Zone D", runZoneD)
    m.add_state("Zone E", runZoneE)
    m.add_state("End", None, end_state=1)
    m.set_start("Start")
    m.run()