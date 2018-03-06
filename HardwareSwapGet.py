#!/usr/bin/python2
#This script gets deals, offers, and whatever kind of content from /r/hardwareswap and put its into a ".txt" file.

import urllib2
import urllib
import os
from getPosts import getPosts
from formatFixer import formatFixer

config = []
SubReddit = "https://www.reddit.com/r/hardwareswap"
Posts = "https://www.reddit.com/r/hardwareswap/comments"
def loadConfig():
    reference = []
    configFile = open("HSG.conf", "r")
    configs = configFile.read()
    configFile.close()
    index = 0
    def skipComment(index):
        index = configs.find("#", index)
        if(index > 0):
            index = configs.find("\n", index)
    skipComment(index)
    index = configs.find(".Tries: ", index) + 7
    reference.append(configs[index: configs.find("\n", index)])
    skipComment(index)
    index = configs.find(".Dir: ", index) + 6
    reference.append(configs[index: configs.find("\n", index)])
    skipComment(index)
    index = configs.find(".Pages: ", index) + 8
    reference.append(int(configs[index: configs.find("\n", index)]))
    skipComment(index)
    while(configs.find("[>]", index) > 0):
        skipComment(index)
        index = configs.find("[>]", index)
        reference.append(configs[index + 3: configs.find("\n", index)])
        index += 1
    return(reference)
def writeToDatabase(section, result, File):
    os.remove(File)
    with open(File, "a") as db:
        db.write("[" + section.upper() + "]\n")
        for x in result:
            if(x[0] == "+"):
                db.write("Title: " + x[1:] + "\n")
            elif(x[0] == "-"):
                db.write("Link: " + x[1:] + "\n")
        db.close()
def main():
    config = loadConfig()
    try:
        titles, links = getPosts(SubReddit, Posts, config[2], config[0])
    except TypeError as e:
        print("Can't connect to page: {0}".format(e))
    results = []
    for x in config[3:]:
        counter = 0
        for s in titles:
            if(s.find(x) > 0):
                if(s[0] != "-"):
                    results.append("+" + formatFixer(s))
                else:
                    results.append(s)
                results.append("-" + links[counter])
            counter += 1
        writeToDatabase(x, results, config[1])
if __name__ == '__main__':
    main()
