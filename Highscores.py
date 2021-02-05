import json, os

class Highscores(object):
    def __init__(this, filename):
        super(Highscores, this).__init__()
        this.filename = filename
        if not os.path.exists(this.filename): # if datafile does not exist
            with open(this.filename, 'w') as jsonfile:
                json.dump({"data": []}, jsonfile)

        this.load()

    def load(this):
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

    def sort(this): this.data = sorted(this.data, key = lambda i: i["score"]) # sort the list

    def addScore(this, score):
        this.data.append(score)
        this.sort()
        this.data = this.data[0:19] # remove extras if there are any
        this.save()
        this.load()

    def generateList(this):
        text = "Highscores<br>"
        for score in this.data:
            text += "{1} ({0})<br>".format(score["date"], score["score"])
        return text
