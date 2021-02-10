import json, os
from .Utils import formatTime

class Highscores(object):
    def __init__(this, filename):
        super(Highscores, this).__init__()
        this.filename = filename
        this.levelName = None
        if not os.path.exists(this.filename): # if datafile does not exist
            with open(this.filename, 'w') as jsonfile:
                json.dump({"data": {}}, jsonfile)

    def load(this, level):
        this.levelName = level
        with open(this.filename) as jsonfile:
            try:
                this.data = json.load(jsonfile)["data"]
            except Exception as e:
                this.data =  []
                this.save()
        this.sort()

    def save(this):
        with open(this.filename, 'w') as jsonfile:
            data = {"data": this.data}
            json.dump(data, jsonfile)

    def sort(this):
        if not this.levelName in this.data.keys(): this.data[this.levelName] = []
        this.data[this.levelName] = sorted(this.data[this.levelName], key = lambda i: i["time"]) # sort the list

    def addScore(this, score, level):
        this.data[this.levelName].append(score)
        this.sort()
        this.data[this.levelName] = this.data[this.levelName][0:19] # remove extras if there are any
        this.save()
        this.load(level)

    def generateList(this, legacy=None):
        text = "Highscores<br>"
        for score in this.data[this.levelName]:
            text += f"- {score['time'] if legacy else formatTime(score['time'])} ({score['date']})<br>"
        return text
