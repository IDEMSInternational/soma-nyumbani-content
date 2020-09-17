import  cmsjson
import  os

directory = r'/Users/johnargentino/soma-nyumbani-content/inputs'
for day in os.listdir(directory):
    if day.endswith(".html"):
        string = "inputs/" + day
        path = "/soma-nyumbani-content/outputs/" + day[:-5]
        print(path)
        cmsjson.cmstojson(string)
