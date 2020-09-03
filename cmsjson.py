#reads an csm html file and converts it into a json file in which the headings are converted into elements and the remaining html is preserved
squares = open('squares.html','r')
html_str = ""
for line in squares:
    html_str = html_str + line

json = {}

h1split = html_str.split("<h1><span>")
count = 0
for x in h1split:
    if count == 0:
        print(count)   #code to identify document titles
    else:
        index = x.index("<")
        title = x[0:index] + "--"
        #json[x[:index]= "hi"]
        print(title)
    count = count + 1
    
    





