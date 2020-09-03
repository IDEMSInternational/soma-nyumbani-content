#reads an csm html file and converts it into a json file in which the headings are converted into elements and the remaining html is preserved
squares = open('squares.html','r')
html_str = ""
for line in squares:
    html_str = html_str + line

json = {}

h1split = html_str.split("<h1><span>")
count1 = 0
for x in h1split:
    if count1 == 0:
        print("later")
          #code to identify document titles
    else:
        
        index1 = x.index("<")
        head1 = x[0:index1]
        tail1 = x[index1:]
        #nested process for isolating header2's
        h2split = tail1.split("<h2><span>")
        count2 = 0
        print(head1)
        print("")
        for y in h2split:
            index2 = y.index("<")
            head2 = y[0:index2]
            tail2 = y[index2:]
            print(head2)
            json[head1] = head2

        #json[head1]= tail1 (values of h1's are just html script)
            count2 = count2 + 1
        
        print("")
        print("")
        print("")

    count1 = count1 + 1
    

