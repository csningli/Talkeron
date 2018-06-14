#! /usr/bin/

import xml.etree.ElementTree

class Topic :
    __name = None
    __comment = None
    __children = None
    __content = None
    
    def __init__(self) :
        self.__name = ""
        self.__comment = ""
        self.__children = []
        self.__content = []
        return

    def setName(self, name) :
        self.__name = name
    
    def getName(self) :
        return str(self.__name)
    
    def setComment(self, comment) :
        self.__comment = comment
    
    def getComment(self) :
        return str(self.__comment)

    def addChild(self, topic) :
        self.__children.append(topic) 
    
    def getChildren(self) :
        return self.__children

    def addContent(self, content) :
        self.__content.append(content) 
    
    def getContent(self) :
        return self.__content

def addTopic(topicxml, parent) : 
    topic = Topic()
    
    for item in topicxml :
        if item.tag == "name" :
            topic.setName(item.text)
        if item.tag == "comment" :
            topic.setComment(item.text)
        if item.tag == "topic" :
            addTopic(item, topic)


    topicPath = "./" + topic.getName() + ".html"
    with open(topicPath, 'r') as f :
        for line in f :
            lineSplit = line.strip().split(" ")
            if lineSplit[0] in ["<hr>", "<br>"] :
                continue
            if lineSplit[0] == "<h2>" and lineSplit[2] == "</h2>" :
                if lineSplit[1].strip() == "Topic" :
                    if not lineSplit[3].strip() == topic.getName() :
                        print("Warning. Topic name in html does not coincide with the one given in configuration file.", "Topic in doc.xml:", topic.getName(), "Topic in html:", lineSplit[3].strip())
                if lineSplit[1].strip() == "Comment" :
                    topic.setComment(" ".join(lineSplit[3:]))

            if (lineSplit[0].strip() in ["<p>", "</p>", "<ol>", "</ol>", "<ul>", "</ul>", "<li>", "</li>", "<b>", "</b>", "<font", "<img", "<figure>", "</figure>", "<figcaption>", "</figcaption>"]) or (len(lineSplit[0].strip()) > 0 and not lineSplit[0].strip()[0] == "<"):
                topic.addContent(line.strip())
        

    parent.addChild(topic)
    return

def printTopic(topic, prefix = "") : 
    print(prefix + topic.getName())
    print(prefix + topic.getComment())
    for line in topic.getContent() :
        print(prefix + line)
    for child in topic.getChildren() :
        printTopic(child, prefix + "\t")
    return
 
def writeTopicIndex(topic, ID = "", prefix = "|" + "-" * 10, f = None) : 
    topicid = ID
    if len(ID) > 0 :
        topicid += " | "
    topicid += topic.getName().strip().split()[0]
    f.write(prefix + " <a href=\"#" + topicid +  "\">" + topic.getName() + "</a> : ")
    f.write(topic.getComment() + "\n <br>\n")
    for topic in topic.getChildren() :
        writeTopicIndex(topic, topicid, "&nbsp;" * 10 + prefix, f)
        
    return
    
def writeTopicBody(topic, ID = "", f = None) : 
    topicid = ID
    if len(ID) > 0 :
        topicid += " | "
    topicid += topic.getName().strip().split()[0]
    
    f.write("<hr>\n")
    f.write("<div id=\"" + topicid +  "\" style=\"width:600px\">\n")
    f.write("<h2>" + topicid + "</h2>\n")
    f.write("<b>Comment</b>: " + topic.getComment() + "\n")
    
    for line in topic.getContent() :
        f.write(line.strip() + "\n")
        
    f.write("</div>\n")
    for child in topic.getChildren() :
        writeTopicBody(child, topicid, f)
        
    return
    
def generateMain(root) :
    import time
    with open("./" + time.strftime("%y%m%d%H%M%S") + "-" + root.getName() + ".html", 'w') as f :
        # create the title and headers
        f.write("<html>\n")    
        f.write("<head>\n")    
        f.write("<script type=\"text/javascript\" src=\"http://latex.codecogs.com/latexit.js\"></script>\n")
        f.write("<script type=\"text/javascript\">LatexIT.add('p', true);</script>\n")
        f.write("</head>\n")    
        f.write("<body>\n")    
        f.write("<h1> " + root.getName() + " </h1>\n")    
        f.write("<hr>\n")
        f.write("<br>\n")    
        # create the div for indices 
        for topic in root.getChildren() :
            writeTopicIndex(topic, "",  "|" + "-" * 10, f)
    
        f.write("<br>\n")    
        
        # create the div for topic body
        for topic in root.getChildren() :
            writeTopicBody(topic, "", f)
        
        # end of the main file 
        f.write("</body>\n")    
        f.write("</html>\n")    
        
    return


if __name__ == "__main__" :
    import sys, os, subprocess
    if len(sys.argv) < 2 :
        print("Exit. [There is not enough argument. Usage: python docupdate.py path/to/work_position]")
        exit(1)

    print("Execution of docconfig.py started.")
    
    workPos = sys.argv[1]
    if os.path.isdir(workPos) :
        print("Detected work position:", workPos)
    else :
        print("Exit. [Work position:", workPos, "does not exist.]")
        exit(1)
        

    inputFileName = workPos + "/input.txt"

    if os.path.exists(inputFileName) :
        print("Detected input file: ", inputFileName)
    else :
        print("Exit. [Input file:", inputFileName, "does not exist.]")
        exit(1)


    talkeronHome = None
    projectPath = None
    latexitSrc = None
    
    with open(inputFileName, 'r') as f :
        for line in f :
            lineSplit = line.split("\t")
            if lineSplit[0].strip() == "talkeron" and len(lineSplit) > 1:
                talkeronHome = lineSplit[1].strip() 
            if lineSplit[0].strip() == "projpath" and len(lineSplit) > 1:
                projectPath = lineSplit[1].strip()

    if projectPath is not None and os.path.isdir(projectPath) :
        print("Project: ", projectPath)
    else :
        print("Exit. [Input parameter \"project\" is missing or inavailable.]")
        exit(1)

    os.chdir(projectPath)

    docxmlPath = projectPath + "/doc.xml" 
    docroot = Topic()
    if os.path.exists(docxmlPath) :
        print("Doc configuration file: ", docxmlPath)
        e = xml.etree.ElementTree.parse(docxmlPath).getroot()
        if not e.tag == "doc" :
            print("Incorrect doc configuration.")
        else :
            for item in e :
                if item.tag == "main" :
                    docroot.setName(item.text)
                if item.tag == "source" :
                    docroot.setComment(item.text)
                    os.chdir(projectPath + "/" + docroot.getComment()) # change working directory to the 'source' folder
                if item.tag == "topic" :
                    addTopic(item, docroot)
        # printTopic(docroot)
        os.chdir(projectPath)
        generateMain(docroot)
    else :
        print("No doc configuration. Create one for the project.")
        with open(docxmlPath, 'w') as f :
            f.write("<?xml version = \"1.0\"?>\n")
            f.write("<doc>\n")
            f.write("\t<main></main>\n")
            f.write("\t<source></source>\n")
            f.write("\t<topic>\n")
            f.write("\t\t<name></name>\n")
            f.write("\t</topic>\n")
            f.write("</doc>\n")
        
        print("Now you can edit the configuration file:", docxmlPath)
    
    print("Done.")
