#reads an csm html file and converts it into a session file in which the headings are
#converted into elements and the remaining html is preserved

import json
import os

#below is a dictionary of the "Areas involved", which will be used later for searching the html
#and filling the session dict; search items perhaps should be truncated to account for potential typos
 #

def cms_session_to_json(session):
    h1split = session['doc'].split("<h1 ><span >")
    for x in h1split:
        if x.find("Session Guide: ") != -1:
            session["type"] = "Session Guide"
            titleindex = x.find("Session Guide: ") + len("Session Guide: ")
            penpiece = x[titleindex:].split("<")[0]
            session["title"] = penpiece
        elif x.find("Session Guide</span><span >: ") != -1:
            session["type"] = "Session Guide"
            titleindex = x.find("Session Guide</span><span >: ") + len("Session Guide</span><span >: ")
            penpiece = x[titleindex:].split("<")[0]
            session["title"] = penpiece

        #code to identify document titles
        if x.find("</span></h1>") != -1:
            index1 = x.index("</span></h1>")
            head1 = x[0:index1]
            #specific measures need to be taken for Activities, namely stripping out the "Activity: " 
            # portion of the header, and (as of now) making Activity its type
            act = "Activity: "
            if head1.find(act) != -1:
                head1 = x[len(act):index1]
                session[format_key(head1)] = {}
                session[format_key(head1)]["type"] = "Activity"
            else:
                session[format_key(head1)] = {}
            tail1 = x[index1 + len("</span></h1>"):]

            #nested process for isolating header2's
            h2split = tail1.split("<h2 ><span >")
            #add entry to session dict that has h1 as a key and an open dict (to be filled with h2 and corresponding html) as value 
            count2 = 0
            for y in h2split:
                if count2 != 0:
                    index2 = y.index("</span></h2>")
                    head2 = y[0:index2]

                    tail2 = y[index2 + len("</span></h2>"):]
                    if tail2.find("This work is licensed by IDEMS International") != -1:
                        scrapindex = tail2.index("This work is licensed by IDEMS International")
                        tail2 = y[index2 + len("</span></h2>"):(scrapindex-6)]
                    if head1 == "Session Outline" and head2 == "Areas involved":
                        session[format_key(head2)]= {}
                        ulsplit = tail2.split("<ul >")
                        countul = 0
                        count3 = 0
                        head3 = "first"
                        for act in ulsplit:
                            if countul != 0:
                                lisplit = act.split("<li ><span >")
                                countli = 0
                                for li in lisplit:
                                    if countli != 0:
                                        liindex = li.index("</span></li>")
                                        lihead = li[:liindex]
                                        if countul % 2 != 0:
                                            session[format_key(head2)][format_key(lihead)]= {}
                                            head3 = lihead
                                        else:
                                            count3 += 1
                                            session[format_key(head2)][format_key(head3)][format_key(lihead)] = count3
                                    countli += 1
                            countul += 1
                    elif head1 == "Session Outline" and head2 == "Description":
                        session[format_key(head2)]=tail2
                    else:
                        session[format_key(head1)][format_key(head2)]=tail2
                count2 = count2 + 1   

        #session[format_key(head1)]= tail1 (values of h1's are just html script)

    session["slug"] = format_slug(session["title"])
    del session['doc']
    return session

# convert string to lower case and replace spaces with underscores for use
# as json object database keys
def format_key(text: str) -> str:
    return "_".join(text.lower().strip().split(" "))

# similar to format_key, but use '-' instead of '_'
def format_slug(text: str) -> str:
    return "-".join(text.lower().strip().split(" "))    



#remains to be done: 
#                    delete html prefix with h2
#                    process \n's
