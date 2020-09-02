#reads an csm html file and converts it into a json file in which the headings are converted into elements and the remaining html is preserved
squares = open('squares.html','r')
html_str = ""
for line in squares:
    html_str = html_str + line
    
h1split = html_str.split("h1")
for x in h1split:
    print(x)






