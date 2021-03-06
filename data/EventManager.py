import pygame

class EventManager(object):
    def __init__(this):
        super(EventManager, this).__init__()
        this.eventList = []
        this.time = None

    def addEvent(this, name, callback, time):
        if time <= 0:
            raise ValueError
        event = {}
        event["name"] = name
        event["callback"] = callback
        event["time"] = time
        event["lastTime"] = pygame.time.get_ticks()
        this.eventList.append(event)

    def removeEvent(this, name):
        i = this.findIndexByName(name)
        this.eventList.pop(i)

    def findIndexByName(this, name):
        for i in range(len(this.eventList)):
            if this.eventList[i]["name"] == name:
                return i
        raise KeyError

    def editEvent(this, name, callback, time):
        if time <= 0:
            raise ValueError
        this.eventList[this.findIndexByName(name)] = {
            "name": name,
            "callback": callback,
            "time": time,
            "lastTime": this.eventList[this.findIndexByName(name)]["lastTime"]
        }

    def checkEvents(this, time):
        if not this.time: this.time = time
        for event in this.eventList:
            if time > event["lastTime"] + event["time"]:
                event["lastTime"] = time
                event["callback"]()

EVENTMANAGER =  EventManager()
