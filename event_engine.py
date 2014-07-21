#!/usr/bin/env python
#-*- coding: utf-8 -*-

import copy
import pprint

def __engine_callback__(old_val, new_val):
    """ OVERRIDE ME, this function is called 
    for each scope attribute change """
    #OVERRIDE ME do something
    pass

class Engine(object):
    def add(self, attribute, custom_callback = False):
        """ add a callback to a scope attribute, 
        default = __engine_callback__ """
        if not attribute in self.__dict__:
            self.__dict__[attribute] = [__engine_callback__]
        else:
            if custom_callback:
                self.__dict__[attribute].append(custom_callback)

    def remove(self, attribute, custom_callback):
        """ remove a callback from a scope attribute """
        if custom_callback in self.__dict__[attribute]:
            self.__dict__[attribute].remove(custom_callback)

    def unwatch(self, attribute):
        """ disable all callbacks calls for 
        all changes in a specific scope attribute """
        self.__dict__[attribute] = {'unwatch': self.__dict__[attribute]}

    def watch(self, attribute):
        """ enable all callback previusly 
        defined for all changes in specific scope attribute"""
        if 'unwatch' in self.__dict__[attribute]:
            self.__dict__[attribute] = self.__dict__[attribute]['unwatch']

    def call(self, attribute, old_val, new_val):
        """ call all callback when a attribute value of scope change 
            only if this scope attribute is watched"""
        if not 'unwatch' in self.__dict__[attribute]:
            for callback in self.__dict__[attribute]:
                callback(old_val, new_val)


class RootScope(object):
    """RootScope"""
    engine = Engine()
    _instance = None

    def __init__(self, _watch_repetitions = False):
        """ set event generation for equals values or not """
        self._watch_repetitions = _watch_repetitions
    
    def __new__(cls, *args, **kwargs):
        """ Singleton RootScope """
        if not cls._instance:
            cls._instance = super(RootScope, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __setattr__(self, attribute, value):
        """ called for each change on a scope attribute """
        if not attribute in self.__dict__:
            Scope.engine.add(attribute)
        else:
            if (self.__dict__[attribute] != value) or self._watch_repetitions:
                Scope.engine.call(
                    attribute = attribute, 
                    old_val = self.__dict__[attribute], 
                    new_val = value)
        self.__dict__[attribute] = value

    def add(self, attribute, custom_callback):
        Scope.engine.add(attribute, custom_callback)

    def remove(self, attribute, custom_callback):
        Scope.engine.remove(attribute, custom_callback)

    def remove_all(self, attribute):
        Scope.engine.__dict__[attribute] = [__engine_callback__]

    def unwatch(self, attribute):
        Scope.engine.unwatch(attribute)

    def watch(self, attribute):
        Scope.engine.watch(attribute)

    def __events_list__(self):
        """ list all event defined in this scope """
        return Scope.engine.__dict__

    def __events__(self, attribute):
        """ list all event defined in a scope attribute """
        return Scope.engine.__dict__[attribute]

    def get_events(self, attribute):
        """ print the name off all event defined for this scope attribute"""
        tmp_list = []
        for event in Scope.engine.__dict__[attribute]:
            tmp_list.append(event.func_code.co_name)
        print tmp_list

    def get_events_list(self):
        """ print the name off all event defined for this scope """
        tmp_dict = copy.deepcopy(Scope.engine.__dict__)
        for attribute in tmp_dict:
            for callback in tmp_dict[attribute]:
                tmp_dict[attribute][tmp_dict[attribute].index(callback)] = tmp_dict[attribute][tmp_dict[attribute].index(callback)].func_code.co_name
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(tmp_dict)
        

class Scope(RootScope):
    def __init__(self, _watch_repetitions = False):
        """ set event generation for equals values or not """
        self._watch_repetitions = _watch_repetitions
        self.__setattr__ = RootScope.__setattr__

rootScope = RootScope()
