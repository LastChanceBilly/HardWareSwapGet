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
#Deletes the log file if wanted
def clearLog(delete, File):
    if (delete == "True"):
        try:
            os.remove(File)
            print('File "{0}" removed'.format(File))
        except:
            print('No file "{0}" found'.format(File))
def writeToDatabase(section, result, File):
    #Open the log file
    with open(File, "a+") as db:
        #Just to make the [SECTION] part on the log file
        db.write("[" + section.upper() + "]\n")
        #If it has a + in front, its a title, if it has a -, it's a link
        #But don't add either the + or the -
        for x in result:
            if(x[0] == "+"):
                db.write("Title: " + x[1:] + "\n")
            elif(x[0] == "-"):
                db.write("Link: " + x[1:] + "\n")
        db.close()
def main():
    #Get the options from loadConfig and save it into keywords and options
    keywords, options = loadConfig()
    #try to get the pages with the getPosts method
    try:
        titles, links = getPosts(SubReddit, Posts, int(options["Pages"]), int(options["Tries"]))
    except TypeError as e:
        print("Can't connect to page: {0}".format(e))
    results = []
    #For every keyword
    for x in keywords:
        counter = 0
        for s in titles:
            #See if you find it within the title
            if(s.find(x) > 0):
                #Here's why the + and - stuff from writeToDatabase
                #The s[0] thing is for debbuging, dont pay attention to it
                if(s[0] != "-"):
                    results.append("+" + formatFixer(s))
                else:
                    results.append(s)
                #Add the correspondant link next to the title
                results.append("-" + links[counter])
            #One more title have been processed...
            counter += 1
        #Write the results to the "database" (A fancy name for a .txt file)
        writeToDatabase(x, results, options["Dir"])
if __name__ == '__main__':
    main()
