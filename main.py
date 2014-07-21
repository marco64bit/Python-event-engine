#!/usr/bin/env python
#-*- coding: utf-8 -*-

from event_engine import *
import event_engine
import time

def store_all(o, n):
    open('history','a').write("HOLD {}\tNEW {}\n".format(o, n))

event_engine.__engine_callback__ = store_all

def foo(o, n):
    print "custom ", o, n

def main():
    #create some scope value
    rootScope.pippo = "mamma"
    rootScope.pluto = {"chiave1":12, "chiave2":"20"}
    rootScope.prova = 12
    rootScope.user = ''

    #add prova scope to a callback function
    rootScope.add('prova', foo)

    #change prova to invoke my callback
    rootScope.prova = 2

    #get event list of all scope values
    rootScope.get_events_list()

    #remove my callback from prova
    rootScope.remove('prova', foo)

    #get event list of all scope values egain
    rootScope.get_events_list()

    #get event list of only one scope
    rootScope.get_events('prova')

    #unwatch all event on rootScope.prova
    rootScope.unwatch('prova')

    #print a list of all event on rootScope.prova
    print rootScope.__events__('prova')

    #change prova without watch
    rootScope.prova = "hahahaha!"
    #watch again prova with old watcher
    rootScope.watch('prova')
    #now the value is watched
    rootScope.prova = "ops!"


    rootScope.add('pluto', foo)
    rootScope.get_events('pluto')
    rootScope.pluto = 2
    rootScope.pluto *= 10

    rootScope.get_events_list()

    #remove all watch on pluto
    rootScope.remove_all('pluto')

    #engine now watch equals values
    rootScope._watch_repetitions = True
    rootScope.p = 1
    rootScope.add('p', foo)
    rootScope.p = 1
    rootScope.p = 1

    #create another scope
    scope = Scope()
    scope.prova = "mamma"
    scope.add("prova", foo)
    scope.prova = "wow"

    #create another scope
    scope2 = Scope()
    scope2.prova = "xxx"
    scope2.add("prova", foo)
    scope2.prova = "yyy"
    scope2.prova = "yyy"

    #try to instance singleton rootscope
    rootScope2 = RootScope()
    rootScope.same = "mamma"
    print "Singleton:\t", rootScope2.same == rootScope.same


if __name__ == '__main__':
    main()
