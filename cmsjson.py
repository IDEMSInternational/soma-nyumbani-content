#reads an csm html file and converts it into a session file in which the headings are
#converted into elements and the remaining html is preserved
session = {}
import json
#below is a dictionary of the "Areas involved", which will be used later for searching the html
#and filling the session dict; search items perhaps should be truncated to account for potential typos
areasdict = {
    "Citizenship":[
        "Values Formation",
        "Social Responsibility",
        "Social Entrepreneurship",
        "Religious Activities",
        "Socio-cultural Activities"
    ],
    "Environment":[
        "Personal Hygiene",
        "Hygiene and Conservation",
        "Careers in Science",
        "(Non)Communicable Diseases",
        "Body Systems",
        "Physical Exercise and Safety",
        "Home Remedies and Simple First Aid",
        "Environmental Conservation",
        "Business Resources",
        "Agribusiness"
    ],
    "Creative Arts": [
        "Multi-media cards", # verify spacing between words and dash; powerpoint is confusing
        "Draw and paint pictures",
        "Craft activities",
        "Music and dance",
        "Drama",
        "Videography and photography"
    ],
    "Language": [
        "Language games",
        "Debates",
        "Public speaking",
        "Poetry",
        "Oral Literature",
        "Reading",
        "Writing"
    ],
    "Games and fitness": [
        "Running games",
        "Dancing",
        "Athletics",
        "Aerobics"
    ],
    "Life skills": [
        "Self-aware",
        "Stop Bullying and Violence", #arbitrary capitalization that should be addressed. ooh 
                                     #maybe I can use a lowercase function to account for that
                                     #I have not done that yet (delete when complete)
        "Time Management",
        "Making decisions",
        "Leadership",
        "Communication",
        "Self-esteem",
        "Conflict resolution",
        "Choosing subjects and careers",
        "Study and organisational skills", #there's a comma after this item in the powerpoint
        "Goal setting",
        "Daily Living Skills"
    ],
    "Home science": [
        "Personal hygiene",
        "Clothes",
        "Foods",
        "Care of the home and compound",
        "Consumer awareness"
    ],
    "Mathematics and Financial literacy": [
        #In the powerpoint there are two subheaders with respective lists
        #For now, I am treating it all as one list
        "Geometry shapes",
        "Math Brain Teasers",
        "Trick Questions",
        "Riddles",
        "Ratios and Proportions",
        "The Number System",
        "Expressions and Equations",
        "Self-assessment",
        "Self-discovery" #What do these last two have to do with financial literacy?
    ]
}

htmlfile = open('squares.html','r')
html_str = ""
for line in htmlfile:
    html_str = html_str + line



h1split = html_str.split("<h1><span>")
count1 = 0
for x in h1split:
    if count1 == 0:
        if x.find("Session Guide") != -1:
            session["type"] = "Session Guide"
            titleindex = x.find("Session Guide: ") + len("Session Guide: ")
            penpiece = x[titleindex:].split("<")[0]
            session["title"] = penpiece

          #code to identify document titles
    else:
        
        index1 = x.index("</span></h1>")
        head1 = x[0:index1]
        #specific measures need to be taken for Activities, namely stripping out the "Activity: " 
        # portion of the header, and (as of now) making Activity its type
        act = "Activity: "
        if head1.find(act) != -1:
            head1 = x[len(act):index1]
            session[head1] = {}
            session[head1]["type"] = "Activity"
        else:
            session[head1] = {}
        tail1 = x[index1 + len("</span></h1>"):]
        #print(head1)
        #nested process for isolating header2's
        h2split = tail1.split("<h2><span>")
        #add entry to session dict that has h1 as a key and an open dict (to be filled with h2 and corresponding html) as value 
        count2 = 0
        for y in h2split:
            if count2 != 0:
                index2 = y.index("</span></h2>")
                head2 = y[0:index2]
                tail2 = y[index2 + len("</span></h2>"):]
                if head1 == "Session Outline" and head2 == "Areas involved":
                    session[head2]= {}
                    ulsplit = tail2.split("<ul>")
                    countul = 0
                    count3 = 0
                    head3 = "first"
                    #print(tail2)
                    for act in ulsplit:
                        if countul != 0:
                            lisplit = act.split("<li><span>")
                            countli = 0
                            for li in lisplit:
                                #print(li)
                                if countli != 0:
                                    liindex = li.index("</span></li>")
                                    lihead = li[:liindex]
                                    #print(lihead + " " + str(countul)) 
                                    if countul % 2 != 0:
                                        session[head2][lihead]= {}
                                        head3 = lihead
                                    else:
                                        count3 += 1
                                        session[head2][head3][lihead] = count3
                                countli += 1
                        countul += 1
                elif head1 == "Session Outline" and head2 == "Description":
                    session[head2]=tail2
                else:
                    session[head1][head2]=tail2
                #print(head2)
            count2 = count2 + 1   

        #session[head1]= tail1 (values of h1's are just html script)
    



    count1 = count1 + 1
    #print("")
    #print("")
    #print("")
#print(session["Session Outline"]["Areas involved"])



with open('script.json', 'w') as outfile:
    json.dump(session, outfile)

    



#remains to be done: 
#                    delete html prefix with h2
#                    process \n's
