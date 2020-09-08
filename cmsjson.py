#reads an csm html file and converts it into a json file in which the headings are converted into elements and the remaining html is preserved
json = {}


squares = open('squares.html','r')
html_str = ""
for line in squares:
    html_str = html_str + line



h1split = html_str.split("<h1><span>")
count1 = 0
for x in h1split:
    if count1 == 0:
        if x.find("Session Guide") != 1:
            json["type"] = "Session Guide"
            titleindex = x.find("Session Guide: ") + len("Session Guide: ")
            penpiece = x[titleindex:].split("<")[0]
            json["name"] = penpiece

          #code to identify document titles
    else:
        
        index1 = x.index("</span></h1>")
        head1 = x[0:index1]
        #specific measures need to be taken for Activities, namely stripping out the "Activity: " 
        # portion of the header, and (as of now) making Activity its type
        act = "Activity: "
        if head1.find(act) != -1:
            head1 = x[len(act):index1]
            json[head1] = {}
            json[head1]["type"] = "Activity"
        else:
            json[head1] = {}
        tail1 = x[index1:]
        #print(head1)
        #nested process for isolating header2's
        h2split = tail1.split("<h2><span>")
        #add entry to json dict that has h1 as a key and an open dict (to be filled with h2 and corresponding html) as value 
        count2 = 0
        for y in h2split:
            if count2 != 0:
                index2 = y.index("<")
                head2 = y[0:index2]
                tail2 = y[index2:]
                json[head1][head2]=tail2
                #print(head2)
            count2 = count2 + 1   

        #json[head1]= tail1 (values of h1's are just html script)
            count2 = count2 + 1
        


    count1 = count1 + 1
    #print("")
    #print("")
    #print("")
for key in json.keys():
    print(key)




#remains to be done: altering "Activity Guide: 