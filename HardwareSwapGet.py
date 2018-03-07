#!/usr/bin/python2
#This script gets deals, offers, and whatever kind of content from /r/hardwareswap and put its into a ".txt" file.

import urllib2
import urllib
import os
from lib import getPosts
from lib import formatFixer

#Where our script will look for:
SubReddit = "https://www.reddit.com/r/hardwareswap"
Posts = "https://www.reddit.com/r/hardwareswap/comments"

def loadConfig():
    #Configuration keywords, just to find them in the HSG.conf
    keywords = [".Tries: ", ".Dir: ", ".Pages: ", ".Clear_log: ", ".Smt: ", ".Email: ", ".Pass: ", ".SubReddit: ", ".Posts: "]
    #A dictionary for all our options
    options = {}
    #Where all our searching keywords will be stored
    reference = []
    #Open and read Configuration file
    configFile = open("HSG.conf", "r")
    configs = configFile.read()
    configFile.close()
    index = 0
    #Look for all the configuration keywords in the file
    for x in keywords:
        index = configs.find(x) + len(x)
        #Since the keywords have a '.' and a ':' (i.e: .Tries: ), eliminate those
        options[x[1:len(x) -2]] = configs[index: configs.find("\n", index)]
    while(configs.find("[>]", index) > 0):
        #Find all the searching keywords and append them to reference
        index = configs.find("[>]", index)
        reference.append(configs[index + 3: configs.find("\n", index)])
        index += 1
    return(reference, options)
def clearLog(delete, File):
    if (delete == "True"):
        try:
            os.remove(File)
            print('File "{0}" removed'.format(File))
        except:
            print('No file "{0}" found'.format(File))
def writeToDatabase(section, result, File):
    with open(File, "a+") as db:
        db.write("[" + section.upper() + "]\n")
        for x in result:
            if(x[0] == "+"):
                db.write("Title: " + x[1:] + "\n")
            elif(x[0] == "-"):
                db.write("Link: " + x[1:] + "\n")
        db.close()
def main():
    keywords, options = loadConfig()
    try:
        titles, links = getPosts(SubReddit, Posts, int(options["Pages"]), int(options["Tries"]))
    except TypeError as e:
        print("Can't connect to page: {0}".format(e))
    results = []
    #clearLog(options["Clear_log"], options["Dir"])
    for x in keywords[7:]:
        counter = 0
        for s in titles:
            if(s.find(x) > 0):
                if(s[0] != "-"):
                    results.append("+" + formatFixer(s))
                else:
                    results.append(s)
                results.append("-" + links[counter])
            counter += 1
        writeToDatabase(x, results, options["Dir"])
if __name__ == '__main__':
    main()
